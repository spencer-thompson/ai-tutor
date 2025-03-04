const domain = window.location.origin;
const current_page = window.location.pathname;
const institution = window.location.hostname.split(".")[0];

async function getData(url) {
  let response = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
  });
  let resp = await response.json();
  return resp;
}

// async function postData(url, data) {
//   let response = await fetch(url, {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//       "AITUTOR-API-KEY": apiKey,
//       Accept: "application/json",
//     },
//     body: JSON.stringify(data),
//   });
//   let resp = await response.json();
//   return resp;
// }

async function getContext() {
  let user_data = await getData(`${domain}/api/v1/users/self`);

  let activity_stream = await getData(
    `${domain}/api/v1/users/self/activity_stream?only_active_courses=true`,
  );

  let courses_data = await getData(
    `${domain}/api/v1/courses?enrollment_state=active&include[]=concluded&include[]=total_scores&include[]=computed_current_score&include[]=syllabus_body&include[]=public_description&per_page=100`,
  );

  let weekAgo = new Date(new Date() - 604800000);
  let planner = await getData(
    `${domain}/api/v1/planner/items?start_date=${weekAgo.toISOString()}&per_page=100`,
  );

  let todo_items = await getData(
    `${domain}/api/v1/users/self/todo?include[]=ungraded_quizzes`,
  );

  console.log(todo_items);

  let todo_items_count = await getData(
    `${domain}/api/v1/users/self/todo_item_count`,
  );

  console.log(todo_items_count);

  let ccd = courses_data.map(({ id, name, course_code, syllabus_body }) => ({
    id,
    name,
    course_code,
    ...(syllabus_body !== null && { syllabus_body }),
  }));

  for (let i = 0; i < ccd.length; i++) {
    let assignments = await getData(
      `${domain}/api/v1/courses/${ccd[i].id}/assignments?bucket=upcoming&order_by=due_at&include[]=score_statistics`,
    );

    let asg = assignments.map(
      ({
        id,
        name,
        description,
        due_at,
        updated_at,
        points_possible,
        html_url,
        rubric,
        lock_at,
        unlock_at,
        locked_for_user,
        submission_types,
      }) => ({
        id,
        name,
        description,
        ...(due_at !== null && { due_at }),
        updated_at,
        ...(points_possible !== null && { points_possible }),
        html_url,
        ...(rubric?.length > 0 && {
          rubric: rubric.map(({ description, points }) => ({
            description,
            points,
          })),
        }),
        ...(lock_at !== null && { lock_at }),
        ...(unlock_at !== null && { unlock_at }),
        locked_for_user,
        submission_types,
      }),
    );

    ccd[i].assignments = asg;
    ccd[i].institution = institution;

    console.log(ccd[i]);
    // console.log(ccd[i]);

    // postData(`${aitutorUrl}course`, ccd[i]);
    // chrome.runtime.sendMessage({ type: "sendCourse", data: ccd[i] });
  }

  let cleaned_planner_data = planner.map(
    ({
      context_type,
      course_id,
      html_url,
      plannable,
      plannable_date,
      plannable_type,
      submissions,
    }) => ({
      canvas_id: user_data.id,
      context_type: context_type,
      course_id: course_id,
      html_url: html_url,
      title: plannable.title,
      created_at: plannable.created_at,
      updated_at: plannable.updated_at,
      plannable_date: plannable_date,
      plannable_type: plannable_type,
      ...(submissions !== false && {
        excused: submissions.excused,
        graded: submissions.graded,
        has_feedback: submissions.has_feedback,
        late: submissions.late,
        missing: submissions.missing,
        needs_grading: submissions.needs_grading,
        submitted: submissions.submitted,
      }),
    }),
  );

  console.log(cleaned_planner_data);

  let cleaned_user_data = {
    institution: institution,
    canvas_id: user_data.id,
    first_name: user_data.first_name,
    last_name: user_data.last_name,
    avatar_url: user_data.avatar_url,
    courses: courses_data.map(({ id, name, course_code, enrollments }) => ({
      institution: institution,
      id,
      name,
      course_code,
      role: enrollments[0].type,
      ...(enrollments[0].computed_current_score != null && {
        current_score: enrollments[0].computed_current_score,
      }),
      // ...(enrollments[0]?.points_possible !== undefined && {
      //   points_possible: enrollments[0].points_possible,
      // }),
    })),
    planner: cleaned_planner_data,
    activity_stream: activity_stream.map(
      ({
        id,
        type,
        title,
        message,
        html_url,
        course_id,
        created_at,
        updated_at,
        read_state,
        late,
        seconds_late,
        missing,
        score,
        assignment_id,
        assignment,
        submission_comments,
      }) => ({
        id,
        kind: type,
        title,
        ...(message !== null && { message }),
        html_url,
        course_id,
        created_at,
        updated_at,
        read_state,
        ...(late !== undefined && { late }),
        ...(seconds_late !== undefined && { seconds_late }),
        ...(missing !== undefined && { missing }),
        ...(score !== undefined && { score }),
        ...(assignment_id !== undefined && { assignment_id }),
        ...(assignment?.points_possible !== undefined && {
          points_possible: assignment.points_possible,
        }),
        ...(submission_comments?.length > 0 && {
          submission_comments: submission_comments.map(
            ({ author_name, comment }) => ({ author_name, comment }),
          ),
        }),
      }),
    ),
  };
  console.log(cleaned_user_data);

  // postData(`${aitutorUrl}user`, cleaned_user_data);

  // const cookie_data = { sub: cleaned_user_data.canvas_id, uni: institution };
  // chrome.runtime.sendMessage({ type: "setCookie", data: cookie_data });
}

getContext();

const domain = window.location.origin;
const current_page = window.location.pathname;
const institution = window.location.hostname.split(".")[0];
const aitutorUrl = process.env.REQUEST_URL;
const apiKey = process.env.API_KEY;
const apiKeyName = process.env.API_KEY_NAME;

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

async function postData(url, data) {
  let response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "AITUTOR-API-KEY": apiKey,
      Accept: "application/json",
    },
    body: JSON.stringify(data),
  });
  let resp = await response.json();
  return resp;
}

async function getContext() {
  let user_data = await getData(`${domain}/api/v1/users/self`);
  // let courses_data = await getData(
  //   `${domain}/api/v1/users/self/courses?enrollment_state=active`,
  // );
  // TODO: loop through course ids and make requests to canvas
  // then send all data back to server probably need new endpoints
  let activity_stream = await getData(
    `${domain}/api/v1/users/self/activity_stream?only_active_courses=true`,
  );

  let courses_data = await getData(
    `${domain}/api/v1/courses?enrollment_state=active&include[]=concluded&include[]=total_scores&include[]=computed_current_score&include[]=syllabus_body&include[]=public_description&per_page=100`,
  );
  // NOTE: enrollments: (example)
  // computed_current_grade: null
  // computed_current_letter_grade: null
  // computed_current_score: 97.3
  // computed_final_grade: null
  // computed_final_score: 52.17
  // enrollment_state: "active"
  // limit_privileges_to_course_section: false
  // role: "StudentEnrollment"
  // role_id: 626
  // type: "student"
  // user_id: 1948325

  // let weekAgo = new Date(new Date() - 604800000);
  // let assignments = await getData(
  //   `${domain}/api/v1/planner/items?start_date=${weekAgo.toISOString()}&per_page=75`,
  // );

  let ccd = courses_data.map(({ id, name, syllabus_body }) => ({
    institution: institution,
    id,
    name,
    ...(syllabus_body !== null && { syllabus_body }),
  }));

  for (let i = 0; i < ccd.length; i++) {
    let assignments = await getData(
      `${domain}/api/v1/courses/${ccd[i].id}/assignments?bucket=upcoming&order_by=due_at&include[]=score_statistics`,
    );
    // TODO: Add assignments

    postData(`${aitutorUrl}course`, ccd);
  }

  let cleaned_user_data = {
    institution: institution,
    canvas_id: user_data.id,
    first_name: user_data.first_name,
    last_name: user_data.last_name,
    avatar_url: user_data.avatar_url,
    courses: courses_data.map(({ id, name, enrollments }) => ({
      id,
      name,
      role: enrollments[0].type,
      current_score: enrollments[0].computed_current_score,
    })),
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
  // console.log(cleaned_user_data);

  postData(`${aitutorUrl}v1/ingest`, cleaned_user_data);
}

getContext();

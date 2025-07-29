# Integrating Large Language Models into Educational Applications: Architecture, Challenges, and Lessons from AI Tutor Development

- RQ1: How can LLMs be efficiently integrated into educational tutoring applications under resource constraints?

The main response here is that the LLM System message is probably the most important piece.
Many hours were spent crafting our system message which I will paste bellow.

```python
    added_bio = f'## Customization\n\n"{bio}"\n- From the user' if bio else ""
    added_descriptions = (
        f"## Courses\n\nYou are an expert tutor in these courses: \n{descriptions}" if descriptions else ""
    )
    return [
        {
            "role": "developer",
            "content": f"""
    # Instructions

    You are an AI Tutor for Utah Valley University with a bright and excited attitude and tone.
    Respond in a concise and effictive manner. Format your response in github flavored markdown.

    {added_descriptions}

    {added_bio}

    ## Current Date and Time

    * {datetime.now(tz=timezone(timedelta(hours=-7))).strftime("%H:%M on %A, %Y-%m-%d")}

    """,
        }
    ]
```

The bio, is instructions or information from the user themselves, further every single course
in the database had a description added to the system message which made the tutor "an expert"
in those courses.

- RQ2: What technical design choices optimize usability, response quality, and cost-effectiveness in small-scale AI Tutor systems?

There were really three things that truly helped here.

1. Tool use: giving the AI the ability to browse the web, look at canvas, and see student data made
  response much ore unique and personal.
2. Clever manipulation of the system message: Putting course details, and code into the system message
  (as shown above) made the tutors responses very uniquely tailored to each user.
3. We used different models when certain questions or messages didn't need an expensive model to use.
  We used a model that was 1/5th cost when possible to reduce costs.
  AND used a database to store information about students to reduce token use.

- RQ3: What were the main challenges and lessons learned during the integration of LLMs for educational purposes? 

Hallucinations were really quite tough. The LLM would often make up things that were completely false.
Through a lot of refinement we managed to get the AI to call tools when necessary to pull from the database
so that it would not makeup so many things.

Another challenge was once again, getting the tutor to provide the kind of answers that we really wanted it to provide
when asked a question. Many students praised the tutor for helping "teach" them, instead of just giving them the answers
which was a very difficult behavior to refine.


The main points of interest that make our tutor so good are:

1. Dynamic Concise Well Crafted System Message
2. Prolific use of Tool Calls and Functions
3. Intuitive user interface

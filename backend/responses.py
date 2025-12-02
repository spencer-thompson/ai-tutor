"""
             _ ._  _ , _ ._
           (_ ' ( `  )_  .__)
         ( (  (    )   `)  ) _)
        (__ (_   (_ . _) _) ,__)
            `~~`\\' . /`~~`
            ,::: ;   ; :::,
           ':::::::::::::::'
 _______________/_ __ \\______________
|                                     |
| This is the epic new API for OPENAI |
|_____________________________________|
"""

import asyncio
import json
import logging
import os
import re
import time
from datetime import datetime, timedelta, timezone
from typing import Dict, List

# from pprint import pprint
from httpx import AsyncClient
from markdownify import markdownify as md
from openai import AsyncOpenAI

from models import Message

logger = logging.getLogger("uvicorn")

MODEL = "gpt-5.1"
SMALL_MODEL = "gpt-5-mini"
PATTERNS = [  # patterns for converting latex to markdown math
    {"rgx": re.compile(r"\\\s*?\(|\\\s*?\)", re.DOTALL), "new": r"$"},
    {"rgx": re.compile(r"\\\s*?\[|\\\s*?\]", re.DOTALL), "new": r"$$"},
]

openai = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)


# added_descriptions = (
#     f"## Courses\n\nYou are an expert tutor in these courses: \n{descriptions}" if descriptions else ""
# )


def general_system_message(bio: str = "", descriptions: str = "") -> str:
    added_bio = f'## Customization\n\n"{bio}"\n- From the user' if bio else ""
    added_descriptions = (
        f"## Courses\n\nYou are an expert tutor in these courses: \n{descriptions}" if descriptions else ""
    )
    return f"""
    # Instructions

    You are the AI Tutor for **Utah Valley University** with a bright and excited attitude and tone.
    Respond in a concise and effictive manner.

    ## Formatting

    Formatting re-enabled — please use Markdown **bold**, _italics_, and header tags to **improve the readability** of your responses.

    {added_bio}

    {added_descriptions}

    ## Current Date and Time

    * {datetime.now(tz=timezone(timedelta(hours=-7))).strftime("%H:%M on %A, %Y-%m-%d")}
    """


def tutor_system_message():
    return """

    ## Tutoring

    When the student asks a question, do not respond with the answer.
    **Instead**, use the socratic method to tutor them and guide their thought process.

    Your responses should guide the student to learn the material in a fun, effective and friendly manner.
    Help the student think by asking one or two guiding questions.
    """


agent = {
    "name": "agent",
    "local": True,
    "func": None,
    "tool": {
        "type": "function",
        "name": "agent",
        "description": """
            Based on the user message, indicate which agent is needed to properly respond.
            If the user is asking a question related to coursework, or without providing context
            choose the Tutor agent, otherwise pick what seems best.
            If the user is asking to search the web use the assistant agent.
            Additionally, choose how much reasoning would be needed to effectively help the user,
            and how verbose, or long the output should be.
            """,
        "parameters": {
            "type": "object",
            "properties": {
                "agent": {
                    "type": "string",
                    "description": "Which agent to choose from.",
                    "enum": ["Tutor", "Friend", "Assistant"],
                },
                "reasoning": {
                    "type": "string",
                    "description": "How much thinking time would provide the best response.",
                    "enum": ["none", "low", "medium", "high"],
                },
                "verbosity": {
                    "type": "string",
                    "description": "How long of a response would be best. Most times lower is better.",
                    "enum": ["low", "medium", "high"],
                },
            },
            "required": [
                "agent",
                "reasoning",
                "verbosity",
            ],
        },
    },
}


### MAIN TOOLS ###


async def get_markdown_webpage(urls: list[str]) -> str:
    pat = re.compile(r"(\n){2,}")

    async def get_page(url: str):
        async with AsyncClient() as client:
            r = await client.get(url)
            cleaned_text = pat.subn(r"\n\n", md(r.text))[0]

            return {url: cleaned_text}

    return await asyncio.gather(*[get_page(u) for u in urls], return_exceptions=True)


read_webpage = {
    "name": "read_webpages",
    "local": False,
    "func": get_markdown_webpage,
    "tool": {
        "type": "function",
        "name": "read_webpages",
        "description": """If the user provides a url or several urls,
            use this tool to get the content of the webpage or webpages.""",
        "parameters": {
            "type": "object",
            "properties": {
                "urls": {
                    "type": "array",
                    "description": "The list of urls to get content for.",
                    "items": {
                        "type": "string",
                        "description": "The url to get content for.",
                    },
                },
            },
            "additionalProperties": False,
            "required": [
                "urls",
            ],
        },
    },
}


async def get_overall_grades(context):
    if user_data := context.get("user"):
        overall_grades = [
            {"name": c.get("name"), "code": c.get("course_code"), "grade": c.get("current_score")}
            for c in user_data.get("courses")
        ]

    return json.dumps(overall_grades)


grades = {
    "name": "grades",
    "local": True,
    "func": get_overall_grades,
    "tool": {
        "type": "function",
        "name": "grades",
        "description": "Use this tool if the users asks about a specific course grade or overall grades. Use liberally",
    },
}


async def get_assignments(context):
    """
    Filters for upcoming_assignments assignments, and sorts by due date
    """
    date_format = "%H:%M on %A, %Y-%m-%d"
    upcoming_assignments = []
    completed_assignments = [
        a.get("assignment_id") for a in context.get("activity_stream") if a.get("score") is not None
    ]

    for course in context.get("courses"):
        upcoming_assignments.append(
            [
                {
                    "name": a.get("name"),
                    "description": a.get("description"),
                    "due_at": (datetime.strptime(a.get("due_at"), "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=-7)).strftime(
                        date_format
                    ),
                    "updated_at": (
                        datetime.strptime(a.get("updated_at"), "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=-7)
                    ).strftime(date_format),
                    "points_possible": a.get("points_possible"),
                    "url": a.get("html_url"),
                    "submission_types": a.get("submission_types"),
                }
                for a in course.get("assignments")
                if a.get("id") not in completed_assignments and not a.get("locked_for_user")
            ]
        )

    upcoming_assignments = [
        assignment for course_assignments in upcoming_assignments for assignment in course_assignments
    ]

    upcoming_assignments.sort(key=lambda date: datetime.strptime(date["due_at"], date_format), reverse=True)

    return json.dumps(upcoming_assignments)


assignments = {
    "name": "assignments",
    "local": True,
    "func": get_assignments,
    "tool": {
        "type": "function",
        "name": "assignments",
        "description": """If the user asks about upcoming assignments, use liberally.
            This only returns not yet completed assignments 1 week from today. """,
    },
}


async def get_activity_stream(context, activities):
    matches = []
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    for activity in context.get("activity_stream"):
        if activity["kind"] in activities:
            matches.append(activity)

    matches.sort(key=lambda date: datetime.strptime(date["updated_at"], date_format), reverse=True)

    return json.dumps(matches)


updates = {
    "name": "updates",
    "local": True,
    "func": get_activity_stream,
    "tool": {
        "type": "function",
        "name": "updates",
        "description": """If the user asks for updates, or information about annoucements, messages,
        submissions, recent assignments, conversations, calendar, graded assignments or discussions. Use liberally.""",
        "parameters": {
            "type": "object",
            "properties": {
                "activities": {
                    "type": "array",
                    "description": "The types of updates to get",
                    "items": {
                        "type": "string",
                        "description": "The type of update to get",
                        "enum": ["Announcment", "Message", "Submission", "Conversation", "DiscussionTopic"],
                    },
                },
            },
            "additionalProperties": False,
            "required": [
                "activities",
            ],
        },
    },
}

### END MAIN TOOLS ###


async def moderate(message: str, user):
    """
    Moderate a string and return a warning if the message is bad.
    """
    response = await openai.moderations.create(
        input=message,
    )

    for result in response.results:
        if result.flagged:
            logger.warning("Flagged for moderation")

            categories = [cat for cat, flg in result.categories.dict().items() if flg]
            if any("self-harm" in c for c in categories):  # check for self-harm and send uvu student resources
                logger.warning(
                    f"STOPPED - {user.get('first_name')} {user.get('last_name')} ({user.get('canvas_id')}) for: self-harm"
                )
                return "I am worried you might not be doing too well, we have some [awesome resources](https://www.uvu.edu/studenthealth/) 🤍"
            if any("sexual" in c for c in categories):  # check for sexual messages and stop them
                logger.warning(
                    f"STOPPED - {user.get('first_name')} {user.get('last_name')} ({user.get('canvas_id')}) for: sexual"
                )
                return "That is not cool bro"
            if any("graphic" in c for c in categories):  # checks for graphic violence
                logger.warning(
                    f"STOPPED - {user.get('first_name')} {user.get('last_name')} ({user.get('canvas_id')}) for: graphic"
                )
                return "[Click here](https://www.uvu.edu/studenthealth/)"

    return ""


tools = [assignments, updates, grades, read_webpage]
# tools = [assignments, grades, python, read_webpage, updates]

tools = {
    tool.get("name"): {
        "tool": tool.get("tool"),
        "func": tool.get("func"),
        "local": tool.get("local"),
    }
    for tool in tools
}

agent_tools = [agent]

agent_tools = {
    tool.get("name"): {
        "tool": tool.get("tool"),
        "func": tool.get("func"),
        "local": tool.get("local"),
    }
    for tool in agent_tools
}


async def openai_formatted_responses_iter(messages: List[Dict[str, Dict]], descriptions, context, role="Auto"):
    completion = ""
    previous_tokens = []
    sliding_window_limit = 3
    async for token in openai_responses_api_iter(
        messages=[{k: dict(m)[k] for k in ("role", "content")} for m in messages],
        descriptions=descriptions,
        context=context,
        role=role,
    ):
        previous_tokens.append(token)
        window_size = len(previous_tokens) if len(previous_tokens) <= sliding_window_limit else sliding_window_limit
        sliding_window = "".join(previous_tokens[-window_size:])

        for pat in PATTERNS:
            if match := pat["rgx"].search(sliding_window):
                previous_tokens = [sliding_window[: match.start()], pat["new"], sliding_window[match.end() :]]

        if len(previous_tokens) >= sliding_window_limit:
            popped_token = previous_tokens.pop(0)  # lol an actual stack in the wild
            completion += popped_token
            # yield popped_token
            yield json.dumps({"content": popped_token})

    if previous_tokens:  # flush out rest of sliding window
        for token in previous_tokens:
            completion += token
            # yield token
            yield json.dumps({"content": token})


async def openai_responses_api_iter(
    messages: List[Message],
    descriptions: str = "",
    context: dict = dict(),
    role: str = "Auto",
    recursive: bool = False,
):
    """
    New Responses API compatible with current code.
    Currently only uses GPT-5 and variants.
    """
    time_start = time.perf_counter()

    # pprint(context)

    if not recursive:
        first_message = messages[-1]
        mod = await moderate(first_message["content"], context.get("user"))  # NOTE: this is a bit messy
        if mod:
            yield mod
            return

    time_after_moderation = time.perf_counter()

    # TODO: add time checks

    course_descriptions = f"## Courses\n\nThese are the student's courses: \n{descriptions}" if descriptions else ""

    if user := context.get("user"):
        bio = user.get("bio")
        if bio is None:
            bio = ""
    else:
        bio = ""

    if role == "Auto":
        agent_router = await openai.responses.create(
            model=MODEL,
            input=messages,
            tools=[t.get("tool") for t in agent_tools.values()],
            instructions=f"""
            Given an input message, determine which agent would most effectively help the user.
            Keep in mind you are providing these parameters for yourself in a future response.

            {course_descriptions}
            """,
            reasoning={"effort": "none"},
            tool_choice="required",
            store=False,  # retrieve later, defaults to true
        )

        # TODO: add time checks

        route = ""
        for output in agent_router.output:
            if output.type == "function_call":
                route = json.loads(output.arguments)
                # TODO: Get tokens used

        logger.info(f"Using Role: {route['agent']}")
        if route["agent"] == "Tutor":
            system_message = general_system_message(bio, descriptions) + tutor_system_message()
        else:
            system_message = general_system_message(bio, descriptions)

        logger.info(f"Using Reasoning: {route['reasoning']}")
        logger.info(f"Using Verbosity: {route['verbosity']}")

    if role == "Quick":
        logger.info("Using Role: Quick")
        route = {
            "reasoning": "none",
            "verbosity": "low",
        }
        system_message = general_system_message(bio, descriptions)

    main_model = MODEL

    stream = await openai.responses.create(
        model=main_model,
        tools=[t.get("tool") for t in tools.values()],
        # tools=[t.get("tool") for t in tools.values()] + [{"type": "web_search"}],
        tool_choice="auto",
        input=messages,
        stream=True,
        instructions=system_message,
        reasoning={"effort": route["reasoning"]},
        text={"verbosity": route["verbosity"]},
        safety_identifier="Spencer",  # should be hashed string, incase they do something crazy
        store=False,  # retrieve later, defaults to true
    )

    tools_called = False
    async for event in stream:
        # print(event.type)
        if event.type == "response.created":
            time_response_created = time.perf_counter()

        if event.type == "response.output_text.delta":
            # print(event.delta, flush=True, end="")
            yield event.delta

        # # NOTE:
        # # This one is if we want the tokens for tool calls as they come in
        # # I don't really wanna mess with that though

        # if event.type == "response.function_call_arguments.delta":
        #     print(event)

        # if "response.output_item" in event.type:
        #     print(event)

        # TODO: Working on this now
        # if "response.web_search_call" in event.type:
        #     print(event)

        # if event.type == "response.web_search_call.completed":
        #     print(event)

        # if event.type == "function_call":
        #     print(event)

        if event.type == "response.function_call_arguments.done":
            logger.info(f"Calling tool: {event}")
            logger.info(f"Calling tool name: {event.name}")
            # print("Calling tool")
            # print(event.arguments)

        if event.type == "response.completed":
            time_response_completed = time.perf_counter()

            # messages += event.response.output
            # print("PRINTING EVENT RESPONSE OUTPUT")
            # pprint(event.response.output)
            for item in event.response.output:
                # print(item)
                if item.type == "function_call":
                    tools_called = True

                    messages.append(
                        {
                            "type": "function_call",
                            "call_id": item.call_id,
                            "name": item.name,
                            "arguments": item.arguments,
                        }
                    )

                    tool_response = await (
                        tools[item.name]["func"](context, **json.loads(item.arguments))
                        if tools[item.name]["local"]
                        else tools[item.name]["func"](**json.loads(item.arguments))
                    )

                    messages.append(
                        {
                            "type": "function_call_output",
                            "call_id": item.call_id,
                            "output": json.dumps({item.name: tool_response}),
                        },
                    )

            tokens_used = {
                "input_tokens": event.response.usage.input_tokens,
                "output_tokens": event.response.usage.output_tokens,
                "reasoning_tokens": event.response.usage.output_tokens_details.reasoning_tokens,
            }

    logger.info(f"Start to end: {time_response_completed - time_start}")
    logger.info(f"Created to end: {time_response_completed - time_response_created}")

    # pprint(messages)
    if tools_called and not recursive:
        async for event in openai_responses_api_iter(
            messages=messages, descriptions=descriptions, context=context, role="Quick", recursive=True
        ):
            yield event

    logger.info(f"Start to end: {time_response_completed - time_start}")
    logger.info(f"Created to end: {time_response_completed - time_response_created}")


async def main() -> None:
    messages = [{"role": "user", "content": "Tell me a joke"}]
    async for event in openai_responses_api_iter(messages):
        print(event, flush=True, end="")


if __name__ == "__main__":
    asyncio.run(main())

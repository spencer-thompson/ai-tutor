"""
If function includes the `local` key,
the first argument of the actual function must be `context`
"""

import asyncio
import json
import logging
import os
import re
from datetime import datetime, timedelta, timezone
from logging.config import dictConfig
from typing import Dict, List

import httpx
from anthropic import AsyncAnthropic
from config import LogConfig
from IPython.core.interactiveshell import InteractiveShell
from markdownify import markdownify as md
from models import Message
from openai import AsyncOpenAI

CHAT_MODEL = os.getenv("CHAT_MODEL")

dictConfig(LogConfig().dict())
logger = logging.getLogger("aitutor")


def system_message(bio: str = "", descriptions: str = ""):
    """
    Includes the current date and time
    """
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


openai = AsyncOpenAI()
anthropic = AsyncAnthropic()


async def get_markdown_webpage(urls: list[str]) -> str:
    pat = re.compile(r"(\n){2,}")

    async def get_page(url: str):
        async with httpx.AsyncClient() as client:
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
        "function": {
            "name": "read_webpages",
            "strict": True,
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
    },
}


async def get_python_result(code: str):
    """
    Execute Python Code
    """
    return InteractiveShell.instance().run_cell(code).result


python = {
    "name": "python",
    "local": False,
    "func": get_python_result,
    "tool": {
        "type": "function",
        "function": {
            "name": "python",
            "strict": True,
            "description": """Use this tool to execute python code. Use if a calculator is needed,
            or to find results for math or calculations. Use only the python standard library.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The python code to execute.",
                    },
                },
                "additionalProperties": False,
                "required": [
                    "code",
                ],
            },
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
        "function": {
            "name": "grades",
            "description": "Use this tool if the users asks about a specific course grade or overall grades. Use liberally",
        },
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
        "function": {
            "name": "updates",
            "strict": True,
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
        "function": {
            "name": "assignments",
            "description": """If the user asks about upcoming assignments, use liberally.
            This only returns not yet completed assignments 1 week from today. """,
        },
    },
}


async def agent():
    pass


async def need_tools(messages: List[dict[str:str]]):
    """
    Check if tools are needed
    """
    response = await openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "need_tools",
                    "strict": True,
                    "description": "True if more information is needed",  # TODO:
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "tools": {
                                "type": "boolean",
                                # "description": "todo",
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "tools",
                        ],
                    },
                },
            }
        ],
        tool_choice="required",
    )

    return json.loads(response.choices[0].message.tool_calls[0].function.arguments)["tools"]


async def moderate(messages: List[Message]):
    response = await openai.moderations.create(
        model="omni-moderation-latest",
        input=messages[-1].content,
    )

    return response.results[0]


tools = [assignments, grades, python, read_webpage, updates]

tools = {
    tool.get("name"): {
        "tool": tool.get("tool"),
        "func": tool.get("func"),
        "local": tool.get("local"),
    }
    for tool in tools
}

PATTERNS = [  # patterns for converting latex to markdown math
    {"rgx": re.compile(r"\\\s*?\(|\\\s*?\)", re.DOTALL), "new": r"$"},
    {"rgx": re.compile(r"\\\s*?\[|\\\s*?\]", re.DOTALL), "new": r"$$"},
]


async def openai_formatted_iter_response(messages: List[Dict[str, Dict]], descriptions, context, model: str = "gpt-4o"):
    completion = ""
    previous_tokens = []
    sliding_window_limit = 3
    async for token in openai_iter_response(messages=messages, descriptions=descriptions, context=context, model=model):
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


async def openai_iter_response(messages: List[Dict[str, Dict]], descriptions, context, model: str = "gpt-4o"):
    logger.info(f"Using Model: {model}")
    mod = await moderate(messages)

    if mod.flagged:
        logger.warning(
            f"Chat Message Flagged: \n{messages[-1].content}\n\n For: {[c for c, f in mod.categories.dict().items() if f]}"
        )
        categories = [cat for cat, flg in mod.categories.dict().items() if flg]
        if any("self-harm" in c for c in categories):
            yield "I am worried you might not be doing too well, we have some [awesome resources](https://www.uvu.edu/studenthealth/) 🤍"
            return
        if any("sexual" in c for c in categories):
            yield "That is not cool bro"
            return
        if any("graphic" in c for c in categories):
            yield "[Click here](https://www.uvu.edu/studenthealth/)"
            return

    if len(context["courses"]) == 0:  # prevent non-necessary context
        tools = [python, read_webpage]
    else:
        tools = [assignments, grades, python, read_webpage, updates]

    bio = context["user"].get("bio")

    tools = {
        tool.get("name"): {
            "tool": tool.get("tool"),
            "func": tool.get("func"),
            "local": tool.get("local"),
        }
        for tool in tools
    }

    response = (
        await openai.chat.completions.create(
            messages=system_message(bio, descriptions) + messages,
            model=model,
            # tools=[t.get("tool") for t in tools.values()] if len(context["courses"]) > 0 else None,
            tools=[t.get("tool") for t in tools.values()],
            tool_choice="auto",
            # logprobs=True,
            stream=True,
            temperature=0.7,  # if model != "o1" else False,
            top_p=0.9,  # if model != "o1" else False,
            # stream_options={"include_usage": True}, # currently errors out
        )
        # if model != "o1"
        # else await openai.chat.completions.create(
        #     messages=system_message(bio, descriptions) + messages,
        #     model=model,
        #     # tools=[t.get("tool") for t in tools.values()] if len(context["courses"]) > 0 else None,
        #     tools=[t.get("tool") for t in tools.values()],
        #     tool_choice="auto",
        #     # logprobs=True,
        #     # stream=True,
        # )
    )

    completion = ""
    tool_calls = []
    async for chunk in response:
        delta = chunk.choices[0].delta
        if delta and delta.content:
            completion += delta.content
            # yield json.dumps({"content": chunk.choices[0].delta.content})
            yield chunk.choices[0].delta.content

        elif delta and delta.tool_calls:
            for tool in delta.tool_calls:
                if len(tool_calls) <= tool.index:
                    tool_calls.append(
                        {
                            "id": "",
                            "type": "function",
                            "function": {"name": "", "arguments": ""},
                        }
                    )

                tc = tool_calls[tool.index]

                if tool.id:
                    tc["id"] += tool.id

                if tool.function.name:
                    tc["function"]["name"] += tool.function.name

                if tool.function.arguments:
                    tc["function"]["arguments"] += tool.function.arguments

    if tool_calls:
        messages.append({"role": "assistant", "content": completion, "tool_calls": tool_calls})

        for tc in tool_calls:
            function_name = tc["function"]["name"]

            if tc["function"]["arguments"]:
                function_args = json.loads(tc["function"]["arguments"])
            else:
                function_args = {}

            logger.info(f"Tool Call: {tc['function']['name']}")

            if tools[function_name]["local"]:
                function_response = await tools[function_name]["func"](context, **function_args)
            else:
                function_response = await tools[function_name]["func"](**function_args)

            messages.append(
                {
                    "tool_call_id": tc["id"],
                    "role": "tool",
                    "name": function_name,
                    "content": str(function_response),
                }
            )

            response = await openai.chat.completions.create(
                messages=system_message(bio, descriptions) + messages,
                # tools=tools if tool else None,
                # tools=[t.get("tool") for t in tools.values()],
                model=CHAT_MODEL,
                logprobs=True,
                stream=True,
                temperature=0.7,
                top_p=0.9,
                # stream_options={"include_usage": True}, # currently errors out
            )

            completion = ""
            async for chunk in response:
                delta = chunk.choices[0].delta

                if delta and delta.content:
                    completion += delta.content
                    # yield json.dumps({"content": delta.content})
                    yield delta.content


async def anthropic_iter_response(messages, context):
    messages = [{"role": m.role, "content": m.content} for m in messages]
    response = await anthropic.messages.create(
        max_tokens=8192,
        system=system_message()[0].get("content"),
        messages=context + messages,
        model="claude-3-5-sonnet-20241022",
        stream=True,
        temperature=0.7,
        top_p=0.9,
    )

    async for event in response:
        if event.type == "content_block_delta":
            # yield json.dumps({"content": event.delta.text})
            yield event.delta.text


if __name__ == "__main__":

    async def main():
        # res = await need_tools([{"role": "user", "content": "hello"}])
        # print(res)
        # print(res.flagged)

        # r = await get_markdown_webpage(["https://wiki.hyprland.org/", "https://wiki.hyprland.org/Configuring/Binds/"])
        # print(r)

        async for token in openai_iter_response(
            [
                {
                    "role": "user",
                    "content": "How do I set repeating binds, here is the documentation https://wiki.hyprland.org/Configuring/Binds/",
                }
            ]
        ):
            print(json.loads(token).get("content"), end="")
            # print(json.loads(token).get("flagged"), end="")
            # print()

    asyncio.run(main())

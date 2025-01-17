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
from typing import List

import httpx
from anthropic import AsyncAnthropic
from config import LogConfig
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
    added_bio = f'## Customization\n"{bio}"\n- From the user' if bio else ""
    added_descriptions = (
        f"## Courses\nYou are an expert tutor in these courses: \n{descriptions}" if descriptions else ""
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


async def get_activity_stream(context, activities):
    matches = []
    for activity in context.get("activity_stream"):
        if activity["kind"] in activities:
            matches.append(activity)

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
            submissions, recent assignments, conversations, calendar, grades or discussions. Use liberally.""",
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
    all_assignments = []
    for course in context.get("courses"):
        all_assignments.append(
            [
                {
                    "name": a.get("name"),
                    "description": a.get("description"),
                    "due_at": (datetime.strptime(a.get("due_at"), "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=-7)).strftime(
                        "%H:%M on %A, %Y-%m-%d"
                    ),
                    "updated_at": (
                        datetime.strptime(a.get("updated_at"), "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=-7)
                    ).strftime("%H:%M on %A, %Y-%m-%d"),
                    "points_possible": a.get("points_possible"),
                    "url": a.get("html_url"),
                    "submission_types": a.get("submission_types"),
                }
                for a in course.get("assignments")
            ]
        )
        # for assignment in course.get("assignments"):
        # all_assignments.append({})

    return json.dumps(all_assignments)


assignments = {
    "name": "assignments",
    "local": True,
    "func": get_assignments,
    "tool": {
        "type": "function",
        "function": {
            "name": "assignments",
            "description": """If the user asks about upcoming assignments, use liberally.
            This only returns assignments 1 week from today. """,
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


tools = [read_webpage, updates, assignments]

tools = {
    tool.get("name"): {
        "tool": tool.get("tool"),
        "func": tool.get("func"),
        "local": tool.get("local"),
    }
    for tool in tools
}


async def openai_iter_response(messages, descriptions, context, model: str = "gpt-4o"):
    logger.info(f"Using Model: {model}")
    mod = await moderate(messages)

    if mod.flagged:
        logger.warning(
            f"Chat Message Flagged: \n{messages[-1].content}\n\n For: {[c for c, f in mod.categories.dict().items() if f]}"
        )
        yield json.dumps({"flagged": mod.flagged})
        return

    if len(context["courses"]) == 0:  # prevent non-necessary context
        tools = [read_webpage]
    else:
        tools = [read_webpage, updates, assignments]

    bio = context["user"].get("bio")

    tools = {
        tool.get("name"): {
            "tool": tool.get("tool"),
            "func": tool.get("func"),
            "local": tool.get("local"),
        }
        for tool in tools
    }

    response = await openai.chat.completions.create(
        messages=system_message(bio, descriptions) + messages,
        model=CHAT_MODEL,
        # tools=[t.get("tool") for t in tools.values()] if len(context["courses"]) > 0 else None,
        tools=[t.get("tool") for t in tools.values()],
        tool_choice="auto",
        logprobs=True,
        stream=True,
        temperature=0.7,
        top_p=0.9,
        # stream_options={"include_usage": True}, # currently errors out
    )

    completion = ""
    tool_calls = []
    async for chunk in response:
        delta = chunk.choices[0].delta
        if delta and delta.content:
            completion += delta.content
            yield json.dumps({"content": chunk.choices[0].delta.content})

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
                    yield json.dumps({"content": delta.content})


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
            yield json.dumps({"content": event.delta.text})


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

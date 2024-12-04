import asyncio
import json
import os
import re
from datetime import datetime
from typing import List

import httpx
from anthropic import AsyncAnthropic
from markdownify import markdownify as md
from models import Message
from openai import AsyncOpenAI

CHAT_MODEL = os.getenv("CHAT_MODEL")
SYSTEM_MESSAGE = [
    {
        "role": "system",
        "content": """
    You are an AI Tutor for Utah Valley University with a bright and excited attitude and tone.
    Respond in a concise and effictive manner. Format your response in github flavored markdown.
    """,
    }
]


def system_message():
    """
    Includes the current date and time
    """
    return [
        {
            "role": "system",
            "content": f"""
    You are an AI Tutor for Utah Valley University with a bright and excited attitude and tone.
    Respond in a concise and effictive manner. Format your response in github flavored markdown.

    The current date and time is {datetime.now().strftime('%H:%M on %A, %Y-%m-%d')}
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


async def get_activity_stream(user):
    pass


updates = {
    "name": "updates",
    "func": get_activity_stream,
    "tool": {
        "type": "function",
        "function": {
            "name": "updates",
            "strict": True,
            "description": """If the user asks for updates, or information about
            annoucements, messages, submissions, recent assignments, conversations or discussions""",
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

tools = [read_webpage]

tools = {
    tool.get("name"): {
        "tool": tool.get("tool"),
        "func": tool.get("func"),
        "local": tool.get("local"),
    }
    for tool in tools
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


async def openai_iter_response(messages, context):
    mod = await moderate(messages)

    if mod.flagged:
        yield json.dumps({"flagged": mod.flagged})
        return

    response = await openai.chat.completions.create(
        messages=system_message() + context + messages,
        model=CHAT_MODEL,
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
                messages=system_message() + context + messages,
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

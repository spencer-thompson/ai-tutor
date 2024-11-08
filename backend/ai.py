import json
import os
from typing import List

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

openai = AsyncOpenAI()


async def agent():
    pass


async def need_tools():
    """
    Check if tools are needed
    """
    pass


async def moderate(text: str):
    response = await openai.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )


async def smart_chat(messages: List[dict[str:str]], context: List[dict[str:str]] = []):
    response = await openai.chat.completions.create(
        messages=SYSTEM_MESSAGE + context + messages,
        model=CHAT_MODEL,
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

            # TODO: Call functions


if __name__ == "__main__":
    import asyncio

    async def main():
        async for token in smart_chat([{"role": "user", "content": "tell me a joke"}]):
            print(json.loads(token).get("content"), end="")

    asyncio.run(main())

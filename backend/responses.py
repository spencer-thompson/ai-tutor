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
import os
import re
import time
from datetime import datetime, timedelta, timezone
from typing import Dict, List

from openai import AsyncOpenAI

from models import Message

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
                    "enum": ["minimal", "low", "medium", "high"],
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


async def moderate(message: str):
    """
    Moderate a string and return a warning if the message is bad.
    """
    response = await openai.moderations.create(
        input=message,
    )

    for result in response.results:
        if result.flagged:
            print("Flagged for moderation")

            categories = [cat for cat, flg in result.categories.dict().items() if flg]
            if any("self-harm" in c for c in categories):  # check for self-harm and send uvu student resources
                # logger.warning(
                #     f"STOPPED - {context['user'].get('first_name')} {context['user'].get('last_name')} ({context['user'].get('canvas_id')}) for: self-harm"
                # )
                return "I am worried you might not be doing too well, we have some [awesome resources](https://www.uvu.edu/studenthealth/) 🤍"
            if any("sexual" in c for c in categories):  # check for sexual messages and stop them
                # logger.warning(
                #     f"STOPPED - {context['user'].get('first_name')} {context['user'].get('last_name')} ({context['user'].get('canvas_id')}) for: sexual"
                # )
                return "That is not cool bro"
            if any("graphic" in c for c in categories):  # checks for graphic violence
                # logger.warning(
                #     f"STOPPED - {context['user'].get('first_name')} {context['user'].get('last_name')} ({context['user'].get('canvas_id')}) for: graphic"
                # )
                return "[Click here](https://www.uvu.edu/studenthealth/)"

    return ""


tools = []

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


async def openai_formatted_responses_iter(messages: List[Dict[str, Dict]], descriptions, context):
    completion = ""
    previous_tokens = []
    sliding_window_limit = 3
    async for token in openai_responses_api_iter(messages=messages, descriptions=descriptions, context=context):
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
    recursive=False,
):
    """
    New Responses API compatible with current code.
    Currently only uses GPT-5 and variants.
    """
    time_start = time.perf_counter()

    # filter out the "name" parameter
    messages = [{k: dict(m)[k] for k in ("role", "content")} for m in messages]
    first_message = messages[-1]

    mod = await moderate(first_message["content"])  # NOTE: this is a bit messy
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

    agent_router = await openai.responses.create(
        model="gpt-5-nano",
        input=messages,
        tools=[t.get("tool") for t in agent_tools.values()],
        instructions=f"""
        Given an input message, determine which agent would most effectively help the user.
        Keep in mind you are providing these parameters for yourself in a future response.

        {course_descriptions}
        """,
        reasoning={"effort": "minimal"},
        tool_choice="required",
        store=False,  # retrieve later, defaults to true
    )

    # TODO: add time checks

    route = ""
    for output in agent_router.output:
        if output.type == "function_call":
            route = json.loads(output.arguments)
            # TODO: Get tokens used

    if route["agent"] == "Tutor":
        print(f"Using Agent: {route['agent']}")
        system_message = general_system_message(bio, descriptions) + tutor_system_message()
    else:
        system_message = general_system_message(bio, descriptions)

    print(f"Using Reasoning: {route['reasoning']}")
    print(f"Using Verbosity: {route['verbosity']}")
    print()

    stream = await openai.responses.create(
        model="gpt-5-nano",
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

        if event.type == "response.function_call_arguments.done":
            print("Calling tool")
            print(event.arguments)

        if event.type == "response.completed":
            time_response_completed = time.perf_counter()

            # print()
            # print(event)

            tokens_used = {
                "input_tokens": event.response.usage.input_tokens,
                "output_tokens": event.response.usage.output_tokens,
                "reasoning_tokens": event.response.usage.output_tokens_details.reasoning_tokens,
            }

    print()
    print()
    print(f"Start to end: {time_response_completed - time_start}")
    print(f"created to end: {time_response_completed - time_response_created}")

    # TODO: add recursive call?
    # Previously this was done on tool calls only


async def main() -> None:
    messages = [{"role": "user", "content": "Tell me a joke"}]
    async for event in openai_responses_api_iter(messages):
        print(event, flush=True, end="")


if __name__ == "__main__":
    asyncio.run(main())

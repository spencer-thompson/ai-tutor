import asyncio
import json
import os
import time
from datetime import datetime, timedelta, timezone

from openai import AsyncOpenAI

openai = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)


def tutor_system_message():
    return """

    ## Tutoring

    When the student asks a question, do not respond with the answer.
    **Instead**, use the socratic method to tutor them and guide their thought process.

    Your responses should guide the student to learn the material in a fun, effective and friendly manner.
    Help the student think by asking one or two guiding questions.
    """


def general_system_message():
    return f"""
    # Instructions

    You are the AI Tutor for Utah Valley University with a bright and excited attitude and tone.
    Respond in a concise and effictive manner. Format your response in github flavored markdown.

    ## Current Date and Time

    * {datetime.now(tz=timezone(timedelta(hours=-7))).strftime("%H:%M on %A, %Y-%m-%d")}
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


async def get_stream(message):
    time_start = time.perf_counter()

    mod = await moderate(message)
    if mod:
        yield mod
        return

    time_after_moderation = time.perf_counter()

    # TODO: add time checks

    agent_router = await openai.responses.create(
        model="gpt-5-nano",
        input=message,
        tools=[t.get("tool") for t in agent_tools.values()],
        instructions="""
        Given an input message, determine which agent would most effectively help the user.
        Keep in mind you are providing these parameters for yourself in a future response.
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
        system_message = general_system_message() + tutor_system_message()
    else:
        system_message = general_system_message()

    # print([t.get("tool") for t in tools.values()])

    print(f"Using Reasoning: {route['reasoning']}")
    print(f"Using Verbosity: {route['verbosity']}")
    print()

    stream = await openai.responses.create(
        model="gpt-5-nano",
        tools=[t.get("tool") for t in tools.values()] + [{"type": "web_search"}],
        tool_choice="auto",
        input=message,
        stream=True,
        instructions=system_message,
        reasoning={"effort": route["reasoning"]},
        text={"verbosity": route["verbosity"]},
        safety_identifier="Spencer",  # should be hashed string, incase they do something crazy
        store=False,  # retrieve later, defaults to true
    )

    async for event in stream:
        # print(event.type)
        # print()
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

            print()
            print(event)

            tokens_used = {
                "input_tokens": event.response.usage.input_tokens,
                "output_tokens": event.response.usage.output_tokens,
                "reasoning_tokens": event.response.usage.output_tokens_details.reasoning_tokens,
            }

    print()
    print()
    print(f"Start to end: {time_response_completed - time_start}")
    print(f"created to end: {time_response_completed - time_response_created}")


async def main() -> None:
    async for event in get_stream(
        "Can you use the web search tool to search the web to find tesla stock current price?"
    ):
        print(event, flush=True, end="")


if __name__ == "__main__":
    asyncio.run(main())

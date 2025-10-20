import asyncio
import os

from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def get_stream():
    stream = await client.responses.create(
        model="gpt-5",
        input="Tell me a joke",
        stream=True,
        instructions="Talk like a pirate",
        reasoning={"effort": "minimal"},
        text={"verbosity": "low"},
    )

    async for event in stream:
        if event.type == "response.output_text.delta":
            # print(event.delta, flush=True, end="")
            yield event.delta


async def main() -> None:
    async for event in get_stream():
        print(event, flush=True, end="")


if __name__ == "__main__":
    asyncio.run(main())

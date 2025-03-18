"""This module contains logic for the llm to select good news."""

import asyncio
import os

from anthropic import AsyncAnthropic

client = AsyncAnthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)


async def main() -> None:
    message = await client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Hello, Claude",
            }
        ],
        model="claude-3-5-sonnet-latest",
    )
    print(message.content)


if __name__ == "__main__":
    asyncio.run(main())

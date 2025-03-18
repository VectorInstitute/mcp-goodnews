import asyncio
import os

import cohere

co = cohere.AsyncClientV2(
    api_key=os.environ.get("COHERE_API_KEY"),
)


async def main() -> None:
    response = await co.chat(
        model="command-r-plus-08-2024",
        messages=[{"role": "user", "content": "hello world!"}],
    )
    print(response)


if __name__ == "__main__":
    asyncio.run(main())

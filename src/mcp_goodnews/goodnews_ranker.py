import json
import os
from typing import Any

import cohere
from cohere.types import ChatMessages

from mcp_goodnews.newsapi import Article

DEFAULT_GOODNEWS_SYSTEM_PROMPT = "Given the list of articles, return {num_articles_to_return} of the most positive articles."
DEFAULT_NUM_ARTICLES_TO_RETURN = 3
DEFAULT_MODEL_NAME = "command-r-plus-08-2024"


class GoodnewsRanker:
    def __init__(
        self,
        model_name: str = DEFAULT_MODEL_NAME,
        num_articles_to_return: int = 3,
        system_prompt_template: str = DEFAULT_GOODNEWS_SYSTEM_PROMPT,
    ):
        self.model_name = model_name
        self.num_articles_to_return = num_articles_to_return
        self.system_prompt_template = system_prompt_template

    def _get_client(self) -> cohere.AsyncClientV2:
        """Get cohere async client.

        NOTE: this requires `COHERE_API_KEY` env variable to be set.
        """
        return cohere.AsyncClientV2(
            api_key=os.environ.get("COHERE_API_KEY"),
        )

    def _format_articles(self, articles: list[Article]) -> str:
        return "\n\n".join(
            json.dumps(a.model_dump(by_alias=True), indent=4) for a in articles
        )

    def _prepare_chat_messages(
        self, articles: list[Article]
    ) -> list[ChatMessages]:
        messages = [
            {
                "role": "system",
                "content": self.system_prompt_template.format(
                    num_articles_to_return=self.num_articles_to_return
                ),
            },
            {
                "role": "user",
                "content": (
                    "Please rank the articles provided below according to their positivity "
                    "based on their `title` as well as the `content` fields of an article."
                    f"\n\n<articles>\n\n{self._format_articles(articles)}</articles>"
                ),
            },
        ]
        return messages

    async def rank_articles(self, articles: list[Article]) -> Any:
        """Uses cohere llms to rank a set of articles."""
        co = self._get_client()
        response = await co.chat(
            model=self.model_name,
            messages=self._prepare_chat_messages(articles),
        )
        return response

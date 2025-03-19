import json
import os
from typing import Any

from cohere import AsyncClientV2
from cohere.types import ChatMessages, ChatResponse

from mcp_goodnews.newsapi import Article

# prompt templates
DEFAULT_GOODNEWS_SYSTEM_PROMPT = (
    "Given the list of articles, rank them based on their positive sentiment. "
    "Return the top {num_articles_to_return} positive articles.\n\n"
    "Please respond with only a JSON string using the format below:\n\n"
    "Do not respond with markdown syntax.\n\n"
    "<output-format>\n\n"
    '{{"articles": [{{"title": ..., "description": ... "url": ... , "urlToImage": ...}}]}}\n\n'
    "</output-format>"
)
DEFAULT_RANK_INSTRUCTION_TEMPLATE = (
    "Please rank the articles provided in JSON format below according to their positivity "
    "based on their `title` as well as the `content` fields of an article.\n\n"
    "\n\n<articles>\n\n{formatted_articles}</articles>"
)

DEFAULT_NUM_ARTICLES_TO_RETURN = 3
DEFAULT_MODEL_NAME = "command-r-plus-08-2024"


class GoodnewsRanker:
    def __init__(
        self,
        model_name: str = DEFAULT_MODEL_NAME,
        num_articles_to_return: int = 3,
        system_prompt_template: str = DEFAULT_GOODNEWS_SYSTEM_PROMPT,
        rank_instruction_template: str = DEFAULT_RANK_INSTRUCTION_TEMPLATE,
    ):
        self.model_name = model_name
        self.num_articles_to_return = num_articles_to_return
        self.system_prompt_template = system_prompt_template
        self.rank_instruction_template = rank_instruction_template

    def _get_client(self) -> AsyncClientV2:
        """Get cohere async client.

        NOTE: this requires `COHERE_API_KEY` env variable to be set.
        """
        return AsyncClientV2(
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
                "content": self.rank_instruction_template.format(
                    formatted_articles=self._format_articles(articles)
                ),
            },
        ]
        return messages

    def _postprocess_chat_response(self, response: ChatResponse) -> str | Any:
        return response.message.content[0].text

    async def rank_articles(self, articles: list[Article]) -> str:
        """Uses cohere llms to rank a set of articles."""
        co = self._get_client()
        response: ChatResponse = await co.chat(
            model=self.model_name,
            messages=self._prepare_chat_messages(articles),
        )
        return self._postprocess_chat_response(response)

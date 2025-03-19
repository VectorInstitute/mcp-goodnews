"""Pydantic BaseModels for NewsAPI.org Response Objects.

This uses the top-headlines API — see https://newsapi.org/docs/endpoints/top-headlines
"""

import os

import httpx
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class ArticleSource(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: str | None = Field(alias="id")
    name: str | None


class Article(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    source: ArticleSource
    author: str | None
    title: str | None
    description: str | None
    url: str | None
    url_to_image: str | None
    published_at: str | None
    content: str | None


class NewsAPIResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    status: str
    total_results: int
    articles: list[Article]


async def get_top_headlines(category: str) -> list[Article]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://newsapi.org/v2/top-headlines",
            params={
                "apiKey": os.environ.get("NEWS_API_KEY"),
                "language": "en",
                "category": category,
            },
        )
        response_json = response.json()
        news_api_response_obj = NewsAPIResponse.model_validate(response_json)

    return news_api_response_obj.articles

"""Pydantic BaseModels for NewsAPI.org Response Objects.

This uses the top-headlines API — see https://newsapi.org/docs/endpoints/top-headlines
"""

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class ArticleSource(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: str = Field(alias="id")
    name: str


class Article(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    source: ArticleSource
    author: str
    title: str
    description: str
    url: str
    url_to_image: str
    published_at: str
    content: str


class NewsAPIResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    status: str
    total_results: int
    articles: list[Article]

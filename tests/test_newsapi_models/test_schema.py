from typing import Any

from mcp_goodnews.newsapi import Article, ArticleSource, NewsAPIResponse


def test_newsapiresponse_from_json(response_json: dict[str, Any]) -> None:
    response = NewsAPIResponse.model_validate(response_json)

    assert response.status == "ok"
    assert response.total_results == 10
    assert all(a.source.id_ == "bbcnews" for a in response.articles)


def test_article_source_serialization(
    example_source_dict: dict[str, Any]
) -> None:
    example_source = ArticleSource.model_validate(example_source_dict)
    serialized = example_source.model_dump(by_alias=True)

    assert serialized == example_source_dict


def test_article_serialization(example_article_dict: dict[str, Any]) -> None:
    example_article = Article.model_validate(example_article_dict)
    serialized = example_article.model_dump(by_alias=True)

    assert serialized == example_article_dict

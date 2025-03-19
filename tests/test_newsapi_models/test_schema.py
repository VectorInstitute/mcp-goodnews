from typing import Any

from mcp_goodnews.newsapi import ArticleSource, NewsAPIResponse


def test_newsapiresponse_from_json(response_json: dict[str, Any]) -> None:
    response = NewsAPIResponse.model_validate(response_json)

    assert response.status == "ok"
    assert response.total_results == 10
    assert all(a.source.id_ == "bbcnews" for a in response.articles)


def test_article_source_serialization() -> None:
    source_dict = {"id": "fake_source_id", "name": "fake_name"}
    source = ArticleSource.model_validate(source_dict)
    serialized = source.model_dump(by_alias=True)

    assert serialized == source_dict

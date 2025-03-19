from typing import Any

from mcp_goodnews.newsapi import NewsAPIResponse


def test_newsapiresponse_from_json(response_json: dict[str, Any]) -> None:
    response = NewsAPIResponse.model_validate(response_json)

    assert response.status == "ok"
    assert response.total_results == 10
    assert all(a.source.id_ == "bbcnews" for a in response.articles)

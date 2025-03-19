from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mcp_goodnews.goodnews_ranker import GoodnewsRanker
from mcp_goodnews.newsapi import NewsAPIResponse
from mcp_goodnews.server import fetch_list_of_goodnews, mcp


@pytest.fixture()
def example_news_response() -> dict[str, Any]:
    return {
        "status": "ok",
        "totalResults": 1,
        "articles": [
            {
                "source": {"id": "fake id", "name": "fake name"},
                "author": "fake author",
                "title": "fake title",
                "description": "fake desc",
                "url": "fake url",
                "urlToImage": "fake url to image",
                "publishedAt": "fake timestamp",
                "content": "fake content",
            },
        ],
    }


@pytest.mark.asyncio
async def test_mcp_server_init() -> None:
    tools = await mcp.list_tools()

    assert mcp.name == "Goodnews"
    assert len(tools) == 1
    assert tools[0].name == "fetch_list_of_goodnews"


@pytest.mark.asyncio
@patch("mcp_goodnews.server.httpx.AsyncClient")
@patch.object(GoodnewsRanker, "rank_articles")
async def test_fetch_list_of_goodnews_tool(
    mock_rank_articles: AsyncMock,
    mock_httpx_async_cm: AsyncMock,
    example_news_response: dict[str, Any],
) -> None:
    # arrange mocks
    mock_rank_articles.return_value = "fake good news"
    mock_httpx_response = MagicMock()
    mock_httpx_response.json.return_value = example_news_response
    mock_httpx_async_client = AsyncMock()
    mock_httpx_async_client.get.return_value = mock_httpx_response
    mock_httpx_async_cm.return_value.__aenter__.return_value = (
        mock_httpx_async_client
    )
    news_api_response_obj = NewsAPIResponse.model_validate(
        example_news_response
    )

    # act
    with patch.dict(
        "os.environ",
        {"NEWS_API_KEY": "fake-news-key", "COHERE_API_KEY": "fake-cohere-key"},
    ):
        await fetch_list_of_goodnews()

    # assert
    mock_rank_articles.assert_awaited_once_with(news_api_response_obj.articles)
    mock_httpx_async_client.get.assert_awaited_once_with(
        "https://newsapi.org/v2/top-headlines",
        params={"apiKey": "fake-news-key"},
    )
    mock_httpx_async_cm.return_value.__aenter__.assert_awaited_once()

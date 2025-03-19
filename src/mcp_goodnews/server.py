"""Goodnews MCP Server"""

import os

import httpx
from mcp.server.fastmcp import FastMCP

from mcp_goodnews.goodnews_ranker import GoodnewsRanker
from mcp_goodnews.newsapi import NewsAPIResponse

# Create an MCP server
mcp = FastMCP("Goodnews")


@mcp.tool()
async def fetch_list_of_goodnews() -> str:
    """Fetch a list of headlines and return only top-ranked news based on positivity."""

    # make request to top-headlines newsapi
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://newsapi.org/v2/top-headlines",
            params={"apiKey": os.environ.get("NEWS_API_KEY")},
        )
        response_json = response.json()
        news_api_response_obj = NewsAPIResponse.model_validate(response_json)

    # rank the retrieved handlines and get only most positive articles
    ranker = GoodnewsRanker()
    goodnews = await ranker.rank_articles(news_api_response_obj.articles)

    return goodnews  # type: ignore[no-any-return]


if __name__ == "__main__":
    mcp.run(transport="stdio")  # pragma: no cover

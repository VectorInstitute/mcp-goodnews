"""Goodnews MCP Server"""


from mcp.server.fastmcp import FastMCP

from mcp_goodnews.goodnews_ranker import GoodnewsRanker
from mcp_goodnews.newsapi import get_top_headlines

# Create an MCP server
mcp = FastMCP("Goodnews")


@mcp.tool()
async def fetch_list_of_goodnews() -> str:
    """Fetch a list of headlines and return only top-ranked news based on positivity."""

    # make request to top-headlines newsapi
    articles = []
    categories = ["science", "health", "technology"]
    for cat in categories:
        top_articles = await get_top_headlines(cat)
        articles.extend(top_articles)

    # rank the retrieved handlines and get only most positive articles
    ranker = GoodnewsRanker()
    goodnews = await ranker.rank_articles(articles)

    return goodnews  # type: ignore[no-any-return]


if __name__ == "__main__":
    mcp.run(transport="stdio")  # pragma: no cover

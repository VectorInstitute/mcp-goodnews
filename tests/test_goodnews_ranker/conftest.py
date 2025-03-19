import pytest

from mcp_goodnews.newsapi import Article, ArticleSource


@pytest.fixture()
def example_articles() -> list[Article]:
    return [
        Article(
            source=ArticleSource(id="1", name="source 1"),
            author="fake author 1",
            title="fake title 1",
            description="fake description 1",
            url="fake url 1",
            url_to_image="fake url to image 1",
            published_at="fake published at 1",
            content="fake content 1",
        ),
        Article(
            source=ArticleSource(id="2", name="source 2"),
            author="fake author 2",
            title="fake title 2",
            description="fake description 2",
            url="fake url 2",
            url_to_image="fake url to image 2",
            published_at="fake published at 2",
            content="fake content 2",
        ),
    ]

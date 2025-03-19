import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from cohere.types import (
    AssistantMessageResponse,
    ChatResponse,
    TextAssistantMessageResponseContentItem,
)

from mcp_goodnews.goodnews_ranker import GoodnewsRanker
from mcp_goodnews.newsapi import Article


def test_goodnews_ranker_init() -> None:
    ranker = GoodnewsRanker(
        model_name="fake model name",
        num_articles_to_return=5,
        system_prompt_template="fake template {name}",
    )

    assert ranker.model_name == "fake model name"
    assert ranker.num_articles_to_return == 5
    assert (
        ranker.system_prompt_template.format(name="alice")
        == "fake template alice"
    )


@patch("mcp_goodnews.goodnews_ranker.AsyncClientV2")
def test_goodnews_get_client(
    mock_async_client_v2: MagicMock,
) -> None:
    ranker = GoodnewsRanker()

    # act
    with patch.dict("os.environ", {"COHERE_API_KEY": "fake-key"}):
        _ = ranker._get_client()

        mock_async_client_v2.assert_called_once_with(api_key="fake-key")


def test_goodnews_format_articles(example_articles: list[Article]) -> None:
    ranker = GoodnewsRanker()

    # act
    formated_str = ranker._format_articles(example_articles)

    assert formated_str == "\n\n".join(
        json.dumps(a.model_dump(by_alias=True), indent=4)
        for a in example_articles
    )


def test_goodnews_prepare_chat_messages(
    example_articles: list[Article],
) -> None:
    ranker = GoodnewsRanker()

    # act
    messages = ranker._prepare_chat_messages(example_articles)

    # assert
    assert len(messages) == 2  # system prompt and user prompt
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    assert ranker._format_articles(example_articles) in messages[1]["content"]


@pytest.mark.asyncio
@patch.object(GoodnewsRanker, "_postprocess_chat_response")
@patch.object(GoodnewsRanker, "_get_client")
async def test_rank_articles(
    mock_get_client: MagicMock,
    mock_postprocess_chat_response: MagicMock,
    example_articles: list[Article],
) -> None:
    # arrange mocks
    fake_chat_response = ChatResponse(
        id="1",
        finish_reason="COMPLETE",
        prompt=None,
        message=AssistantMessageResponse(
            content=[
                TextAssistantMessageResponseContentItem(text="mock response")
            ]
        ),
    )
    mock_async_client = AsyncMock()
    mock_async_client.chat.return_value = fake_chat_response
    mock_get_client.return_value = mock_async_client
    ranker = GoodnewsRanker()

    # act
    await ranker.rank_articles(example_articles)

    # assert
    mock_postprocess_chat_response.assert_called_once_with(fake_chat_response)
    mock_async_client.chat.assert_called_once_with(
        model=ranker.model_name,
        messages=ranker._prepare_chat_messages(example_articles),
    )

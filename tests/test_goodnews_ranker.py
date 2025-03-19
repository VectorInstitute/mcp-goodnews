from unittest.mock import MagicMock, patch

from cohere import AsyncClientV2

from mcp_goodnews.goodnews_ranker import GoodnewsRanker


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


@patch.object(GoodnewsRanker, "_get_client")
def test_goodnews_get_client(mock_get_client: MagicMock) -> None:
    dummy = AsyncClientV2()
    mock_get_client.return_value = dummy
    ranker = GoodnewsRanker()

    # act
    co = ranker._get_client()

    assert co == dummy
    mock_get_client.assert_called_once()

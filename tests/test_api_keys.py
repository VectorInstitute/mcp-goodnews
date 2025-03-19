import importlib
import sys
from unittest.mock import patch

import pytest


@pytest.mark.parametrize(
    ("required_key_name"),
    [("NEWS_API_KEY"), ("COHERE_API_KEY")],
    ids=["newsapi", "cohere"],
)
def test_missing_required_api_key_raises_on_import(
    required_key_name: str,
) -> None:
    with patch.dict("os.environ", {required_key_name: "mock-key"}, clear=True):
        with pytest.raises(ValueError):
            if mcp_goodnews_module := sys.modules.get("mcp_goodnews"):
                importlib.reload(
                    mcp_goodnews_module
                )  # conftest would have already loaded this module
            else:
                importlib.import_module("mcp_goodnews")

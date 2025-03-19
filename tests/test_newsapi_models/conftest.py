import json
from pathlib import Path
from typing import Any, cast

import pytest

EXAMPLE_PATH = Path(__file__).parents[0].absolute()
EXAMPLE_FILENAME = "example_response.json"


@pytest.fixture()
def response_json() -> dict[str, Any]:
    with open(EXAMPLE_PATH / EXAMPLE_FILENAME) as f:
        response_json = json.load(f)
        response_json = cast(dict[str, Any], response_json)
    return response_json  # type: ignore[no-any-return]


@pytest.fixture
def example_source_dict() -> dict[str, Any]:
    return {"id": "fake_source_id", "name": "fake_name"}


@pytest.fixture
def example_article_dict(
    example_source_dict: dict[str, Any]
) -> dict[str, Any]:
    return {
        "source": example_source_dict,
        "author": "fake author",
        "title": "fake title",
        "description": "fake description",
        "url": "fake url",
        "urlToImage": "fake url to image",
        "publishedAt": "fake published at",
        "content": "fake content",
    }

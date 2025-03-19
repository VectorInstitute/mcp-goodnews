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

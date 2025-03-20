import importlib
import sys
from unittest.mock import patch

import pytest

from mcp_goodnews import MISSING_KEY_ERROR_MESSAGES

missing_keys = [(k) for k in MISSING_KEY_ERROR_MESSAGES.keys()]


@pytest.mark.parametrize(
    ("missing_key_name"),
    missing_keys,
    ids=list(MISSING_KEY_ERROR_MESSAGES.keys()),
)
def test_missing_required_api_key_raises_on_import(
    missing_key_name: str,
) -> None:
    # patched os.environ should have missing_key_name removed to raise error
    patched_os_environ = {
        k: k.lower().replace("_", "-")
        for k in MISSING_KEY_ERROR_MESSAGES.keys()
        if k != missing_key_name
    }
    error_msg = MISSING_KEY_ERROR_MESSAGES[missing_key_name]

    with patch.dict("os.environ", patched_os_environ, clear=True):
        with pytest.raises(ValueError, match=error_msg):
            if mcp_goodnews_module := sys.modules.get("mcp_goodnews"):
                importlib.reload(
                    mcp_goodnews_module
                )  # conftest would have already loaded this module
            else:
                importlib.import_module("mcp_goodnews")

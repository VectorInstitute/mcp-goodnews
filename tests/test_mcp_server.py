import pytest

from mcp_goodnews.server import mcp


@pytest.mark.asyncio
async def test_mcp_server_init() -> None:
    tools = await mcp.list_tools()

    assert mcp.name == "Goodnews"
    assert len(tools) == 1
    assert tools[0].name == "fetch_list_of_goodnews"

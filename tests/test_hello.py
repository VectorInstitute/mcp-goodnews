from mcp.server.fastmcp import FastMCP

from mcp_goodnews.server import mcp


def test_mcp() -> None:
    assert isinstance(mcp, FastMCP)

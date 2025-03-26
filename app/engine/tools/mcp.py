from llama_index.core.tools.function_tool import FunctionTool
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from typing import List, Optional

def mcp_get_tools(
    server_url: str,
    allowed_tools: Optional[List[str]] = None,
    **kwargs
):
    """
    Get tools from MCP server.
    
    Args:
        server_url (str): MCP server URL from tools.yaml config.
        allowed_tools (Optional[List[str]]): List of allowed tool names to filter.
    """
    if not server_url:
        raise ValueError("MCP server URL must be configured in tools.yaml")
    
    client = BasicMCPClient(server_url)
    return McpToolSpec(client=client, allowed_tools=allowed_tools).to_tool_list()

def get_tools(**kwargs):
    """
    Get MCP tools.
    """
    return [
        FunctionTool.from_defaults(
            fn=mcp_get_tools,
            name="mcp_get_tools",
            description="Get tools from MCP server",
            **kwargs
        )
    ]

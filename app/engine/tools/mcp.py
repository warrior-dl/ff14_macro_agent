"""MCP Tool integration for LlamaIndex."""
from typing import List, Optional, Dict, Any
import requests
from llama_index.core.tools import FunctionTool
from llama_index.core.tools.tool_spec.base import BaseToolSpec


class BasicMCPClient:
    """Basic client for MCP Server communication."""
    
    def __init__(self, server_url: str):
        self.server_url = server_url
        
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call a tool on the MCP server."""
        response = requests.post(
            f"{self.server_url}/tools/{tool_name}",
            json={"arguments": arguments},
            timeout=30
        )
        response.raise_for_status()
        return response.json()


class McpToolSpec(BaseToolSpec):
    """ToolSpec for MCP Server tools."""
    
    def __init__(
        self, 
        client: BasicMCPClient,
        allowed_tools: Optional[List[str]] = None
    ):
        self.client = client
        self.allowed_tools = allowed_tools
        
    async def to_tool_list_async(self) -> List[FunctionTool]:
        """Get tools from MCP server."""
        # TODO: Implement dynamic tool discovery from MCP server
        tools = []
        if not self.allowed_tools or "fetch_ipinfo" in self.allowed_tools:
            tools.append(FunctionTool.from_defaults(
                self.fetch_ipinfo,
                name="fetch_ipinfo",
                description="Get IP information from MCP server"
            ))
        return tools
        
    def fetch_ipinfo(self, ip: Optional[str] = None) -> Dict[str, Any]:
        """Fetch IP information from MCP server."""
        return self.client.call_tool("fetch_ipinfo", {"ip": ip})


def get_tools(**kwargs) -> List[FunctionTool]:
    """Get MCP tools for integration."""
    client = BasicMCPClient("http://127.0.0.1:8000")
    return McpToolSpec(client).to_tool_list()

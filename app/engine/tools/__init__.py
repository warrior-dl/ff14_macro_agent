import importlib
import os
import logging
from typing import Dict, List, Union
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec

import yaml  # type: ignore
from llama_index.core.tools.function_tool import FunctionTool
from llama_index.core.tools.tool_spec.base import BaseToolSpec

logger = logging.getLogger(__name__)

class ToolType:
    LLAMAHUB = "llamahub"
    LOCAL = "local"
    MCP = "mcp"  # MCP类型

class ToolFactory:
    TOOL_SOURCE_PACKAGE_MAP = {
        ToolType.LLAMAHUB: "llama_index.tools",
        ToolType.LOCAL: "app.engine.tools",
        ToolType.MCP: "app.engine.tools",
    }

    @staticmethod
    async def load_mcp_tools(server_url: str, server_name: str = "default", **kwargs):
        """异步加载MCP工具"""
        logger.info(f"Loading MCP tools from {server_url}")
        client = BasicMCPClient(server_url)
        tools = await McpToolSpec(client=client).to_tool_list_async()
        for tool in tools:
            tool.metadata.name = f"mcp_{server_name}_{tool.metadata.name}"
        logger.info(f"Loaded {len(tools)} MCP tools")
        return tools

    @staticmethod
    async def load_tools(tool_type: str, tool_name: str, config: dict) -> List[FunctionTool]:
        source_package = ToolFactory.TOOL_SOURCE_PACKAGE_MAP[tool_type]
        logger.info(f"Loading tool {tool_name} from {source_package}")
        
        try:
            if tool_type == ToolType.MCP:
                return await ToolFactory.load_mcp_tools(
                    server_url=config.pop('server_url'),
                    server_name=tool_name,
                    **config
                )
            elif "ToolSpec" in tool_name:
                tool_package, tool_cls_name = tool_name.split(".")
                module_name = f"{source_package}.{tool_package}"
                module = importlib.import_module(module_name)
                tool_class = getattr(module, tool_cls_name)
                return tool_class(**config).to_tool_list()
            else:
                module = importlib.import_module(f"{source_package}.{tool_name}")
                tools = module.get_tools(**config)
                if not all(isinstance(tool, FunctionTool) for tool in tools):
                    raise ValueError(f"Invalid tools in module {module}")
                return tools
                
        except ImportError as e:
            raise ValueError(f"Failed to import tool {tool_name}: {e}")
        except AttributeError as e:
            raise ValueError(f"Failed to load tool {tool_name}: {e}")

    @staticmethod
    async def from_env(map_result: bool = False) -> Union[Dict[str, List[FunctionTool]], List[FunctionTool]]:
        tools: Union[Dict[str, FunctionTool], List[FunctionTool]] = {} if map_result else []
        
        if os.path.exists("config/tools.yaml"):
            with open("config/tools.yaml", "r") as f:
                tool_configs = yaml.safe_load(f)
                for tool_type, config_entries in tool_configs.items():
                    for tool_name, config in config_entries.items():
                        loaded_tools = await ToolFactory.load_tools(tool_type, tool_name, config)
                        if map_result:
                            tools.update({tool.metadata.name: tool for tool in loaded_tools})  # type: ignore
                        else:
                            tools.extend(loaded_tools)  # type: ignore
        return tools

# File agent.py

import asyncio
import json
from typing import Any

from dotenv import load_dotenv
from google.adk.agents.llm_agent import LlmAgent
from google.adk.artifacts.in_memory_artifact_service import (
    InMemoryArtifactService,  # Optional
)
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from google.adk.tools.mcp_tool.mcp_session_manager import ( SseConnectionParams, SseServerParams,   # If your package exposes SseServerParameters instead, just swap the name.
)
from google.adk.tools.mcp_tool import MCPToolset

from google.genai import types
from rich import print
load_dotenv()

async def get_tools_async():
    tools, exit_stack = await MCPToolset.from_server(
        connection_params=SseServerParams(
            url="http://localhost:8080/sse",
        )
    )
    print("MCP Toolset created successfully.")
    return tools, exit_stack

async def get_agent_async():
    """Creates an ADK Agent equipped with tools from the MCP Server."""
    tools, exit_stack = await get_tools_async()
    print(f"Fetched {len(tools)} tools from MCP server.")
    root_agent = LlmAgent(
        model="llama3-8b",
        name="weather assistant",
        instruction="Use the tools available to you (especially get_city_weather) to fetch weather data from cities the user asks for.",
        tools=tools,
    )
    return root_agent, exit_stack

root_agent = get_agent_async()


from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import (
    SseConnectionParams,
    SseServerParams,   # If your package exposes SseServerParameters instead, just swap the name.
)

MCP_BASE_URL = "http://localhost:8080/sse"  # 
root_agent = LlmAgent(
    model="llama3-8b",
    name="weather_mcp_client_agent",
    instruction=( "Use the tools available to you (especially get_city_weather) to fetch weather data from cities the user asks for."
    ),
    tools=[
        McpToolset(
            connection_params=SseConnectionParams(
                server_params=SseServerParams(
                    url = MCP_BASE_URL 
                ),
            )
        )
    ],
)

#   instruction="Use the tools available to you(especially get_city_weather) to fetch weather data from cities the user asks for.",



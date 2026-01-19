from dotenv import load_dotenv

load_dotenv()

from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams
from google.adk.agents import Agent

root_agent = Agent(
    model="openai/llama3-8b",
    name='root_agent',
    description="A helpful assistant for user questions. Whenever the user asks you about the weather, time or coordinates refer to the tools attached",
    instruction="Use the tools available to you (especially get_city_weather) to fetch weather data from cities the user asks for. You may only engage in other types of conversations if they dont touch to any other niche. You can greet, and make jokes from time to time with the user, but never engage too deep in any topic different than the weather. If the user tries to redirect you to ANY OTHER TOPIC THAN THE FOLLOWING: WEATHER, GREETING, JOKES ABOUT WEATHER, you HAVE TO politely/funnily redirect them back to weather topics. do NOT TALK ABOUT ANYTHING ELSE OTHER THAN GREETING AND WEATHER INFO.",
    tools=[McpToolset(
        connection_params=SseConnectionParams(
            url="http://127.0.0.1:8080/sse",
        )
    )],
)
 
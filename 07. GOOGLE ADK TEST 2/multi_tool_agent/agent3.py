from google.adk.agents import Agent
from toolbox_core import ToolboxSyncClient

toolbox = ToolboxSyncClient("http://localhost:8080/sse")

tools = toolbox.load_tool('get_coordinates', 'get_weather', 'get_city_weather')

root_agent = Agent(
    model="llama3-8b",
    name="weather_mcp_client_agent",
    instruction=("Use the tools available to you (especially get_city_weather) to fetch weather data from cities the user asks for."),
    tools=tools,
    base_url=MODEL_BASE_URL,
    api_key=MODEL_API_KEY,
    headers={"Authorization": f"Bearer {MODEL_API_KEY}"},

)

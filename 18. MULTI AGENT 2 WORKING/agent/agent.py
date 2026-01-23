import logging
from dotenv import load_dotenv
from google.genai import types
from google.adk.agents.llm_agent import Agent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams
from RAG import before_model_callback, after_model_callback

load_dotenv()

MODEL = "gemini-2.5-flash"

#Tools

def append_to_state(
     tool_context: ToolContext, field: str, response: str
 ) -> dict[str, str]:
     """Append new output to an existing state key.
 
     Args:
         field (str): a field name to append to
         response (str): a string to append to the field
 
     Returns:
         dict[str, str]: {"status": "success"}
     """
     existing_state = tool_context.state.get(field, [])
     tool_context.state[field] = existing_state + [response]
     logging.info(f"[Added to {field}] {response}")
     return {"status": "success"}

#Agents

memory_agent = Agent(
    model=MODEL,
    name='memory_agent',
    description="A helpful assistant for remembering previous conversations. ",
    instruction= "You are a helpful assistant whose job  is to remember what was said during conversations (the current one, and the old ones). " \
    "Use the information provided to check if the memory has relevant info on what the user asked for." \
    "If your memory is empty, just respond normally and acknowledge what the user is telling you " \
    "Only use/respond to what you have been prompted with.",
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
weather_agent = Agent(
    model=MODEL,
    name='weather_agent',
    description="A helpful assistant for user's weather questions. Will not answer anything else. Whenever the user asks you about the weather or coordinates refer to your knowledge",
    instruction= 
        "You are a helpful weather assistant. The user will prompt you with questions about the weather, including a city.\n \
        If the user does not mention a specific city, keep asking them to provide one until they do. Use the tools available to you to fetch weather data from cities the user asks for.\n" \
        "The only tools you have available are :get_coordinates and get_weather. After using the tools, generate a final user response."
        " You may not engage in conversations about anything else.\n " \
        "You can greet, and make jokes from time to time with the user, but NEVER engage in any topic different than the weather.\n" \
        " If the user tries to redirect you to ANY OTHER TOPIC THAN THE FOLLOWING: WEATHER, GREETING, JOKES ABOUT WEATHER, you HAVE TO politely/funnily redirect them back to weather topics.\n" \
        " do NOT TALK ABOUT ANYTHING ELSE OTHER THAN GREETING AND WEATHER INFO. Most importantly you may not make any assumptions about the user's location or intent, and reply in a human way.\n",
    after_model_callback=after_model_callback,
    tools=[McpToolset(
        connection_params=SseConnectionParams(
            url="http://127.0.0.1:8000/sse",
            keepalive=False,
            read_timeout = 0.1,
        )
    ),
    ], 
)

root_agent = Agent(
    model=MODEL,
    name='root_agent',
    description='Greets and Guides the user to more information',
    instruction="""
        You're a friendly secretary. Greet the user using plain text, and ask them if they would like to know more about the weather or previous conversations
    """,
    after_model_callback=after_model_callback,
    generate_content_config=types.GenerateContentConfig(
    temperature=0.5,
    ),
    sub_agents=[weather_agent, memory_agent],
)
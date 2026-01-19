import asyncio
from dotenv import load_dotenv
load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from google.genai import types

from weather_agent import root_agent

async def main():
    session_service = InMemorySessionService()
    artifact_service = InMemoryArtifactService()

    runner = Runner(
        app_name="weather_multi_agent",
        agent=root_agent,
        session_service=session_service,
        artifact_service=artifact_service,
    )

    session = await session_service.create_session(
        user_id="user-1",
        state={},
        app_name="weather_multi_agent",
    )

    content = types.Content(
        role="user",
        parts=[types.Part(text="Weather in Paris?")]
    )

    async for event in runner.run_async(
        session_id=session.id,
        user_id="user-1",
        new_message=content,
    ):
        
        # print
        if getattr(event, "content", None):
            for p in event.content.parts:
                if getattr(p, "text", None):
                    print(f"{event.author}: {p.text}")
                if getattr(p, "function_call", None):
                    fc = p.function_call
                    print(f"!!! Calling {fc.name}({fc.args})")
                if getattr(p, "function_response", None):
                    fr = p.function_response
                    print(f"!!! {fr.name} -> {fr.response}")
        else:
            print(event)

if __name__ == "__main__":
    asyncio.run(main())
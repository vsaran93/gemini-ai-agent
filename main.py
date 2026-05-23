import asyncio

from my_agent.agent import capital_agent

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


APP_NAME = "capital_app"
USER_ID = "user1"
SESSION_ID = "session1"


async def main():

    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    runner = Runner(
        agent=capital_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    print("Agent started.\n")

    while True:

        user_input = input("Ask: ")

        if user_input.lower() == "exit":
            break

        content = types.Content(
            role="user",
            parts=[types.Part(text=user_input)],
        )

        events = runner.run(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=content,
        )

        for event in events:
            if event.content and event.content.parts:
                print("Agent:", event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(main())
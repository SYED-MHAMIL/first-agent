import os
from dotenv import load_dotenv
from typing import cast, List
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from agents.tool import function_tool

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GOOGLE_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

@cl.set_starters  # type: ignore
async def set_starts() -> List[cl.Starter]:
    return [
            cl.Starter(
            label="Morning routine ideation",
            message="Can you help me create a personalized morning routine that would help increase my productivity throughout the day? Start by asking me about my current habits and what activities energize me in the morning.",
            icon="/public/idea.svg",
        ),

        cl.Starter(
            label="Explain superconductors",
            message="Explain superconductors like I'm five years old.",
            icon="/public/learn.svg",
        ),
        cl.Starter(
            label="Python script for daily email reports",
            message="Write a script to automate sending daily email reports in Python, and walk me through how I would set it up.",
            icon="/public/terminal.svg",
            command="code",
        ),
        cl.Starter(
            label="Text inviting friend to wedding",
            message="Write a text asking a friend to be my plus-one at a wedding next month. I want to keep it super short and casual, and offer an out.",
            icon="/public/write.svg",
        )
    ]


@function_tool
@cl.step(type="weather tool")
def get_weather(location: str, unit: str = "C") -> str:
  """
  Fetch the weather for a given location if the  word is misspell first correct it , returning a short description.
  """
  # Example logic
  return f"The weather in {location} is 22 degrees {unit}."


@cl.on_chat_start
async def start():
    #Reference: https://ai.google.dev/gemini-api/docs/openai
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )
    """Set up the chat session when a user connects."""
    
    cl.user_session.set("chat_history" , [])    
    cl.user_session.set('config',config)
    agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant", model=model)
    agent.tools.append(get_weather)
    cl.user_session.set("agent",agent)

    await cl.Message(content="Welcome to the Panaversity AI Assistant! How can I help you today?").send()



@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages and generate responses."""
    # Send a thinking message
    msg=  cl.Message(content = "Thinging...")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))
    
    history =  cl.user_session.get("chat_history") or []
    history.append({"role": "user", "content": message.content})
    
    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
        result = Runner.run_sync(agent, history, run_config=config)
        
        response_content = result.final_output
        
        # Update the thinking message with the actual response
        msg.content = response_content
        await msg.update()

        # Append the assistant's response to the history.
        history.append({"role": "developer", "content": response_content })

        # Update the session with the new history.
        cl.user_session.set("chat_history", history)
        
        # # Optional: Log the interaction
        # print(f"User: {message.content}")
        # print(f"Assistant: {response_content}")
        
    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")



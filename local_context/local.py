import asyncio
from dataclasses import dataclass
import os

from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,RunContextWrapper, Runner,set_tracing_disabled, function_tool
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
gemini_api_key: str | None = os.environ.get("GOOGLE_API_KEY")

set_tracing_disabled(disabled=True)
external_client: AsyncOpenAI = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
llm_provider : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model='gemini-2.5-flash', openai_client=external_client) 



# Define a simple context using a dataclass
@dataclass
class UserInfo:  
    name: str
    uid: int

# A tool function that accesses local context via the wrapper
@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:  
    return f"User {wrapper.context.name} is 47 years old"



async def main():
    # Create your context object
    user_info = UserInfo(name="John", uid=123)  

    # Define an agent that will use the tool above
    agent = Agent[UserInfo](  
        name="Assistant",
        tools=[fetch_user_age],
        model= llm_provider
    )

    # Run the agent, passing in the local context
    result = await Runner.run(
        starting_agent=agent,
        input="What is the age of member?",
        context=user_info,
    )

    print(result.final_output)  # Expected output: The user John is 47 years old.

if __name__ == "__main__":
    asyncio.run(main())
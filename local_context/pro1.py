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


    
@dataclass
class UserInfo:  
    name: str
    uid: int

# A tool function thats accesses local context via the wrapper
@function_tool
async def search(local_context: RunContextWrapper[UserInfo]) -> str:  
    
    await asyncio.sleep(1)
    ctx = local_context.context
    return f"Found tutors in Karachi for user {ctx.name} (uid={ctx.uid})"

async def special_prompt(special_context:RunContextWrapper[UserInfo],agent:Agent[UserInfo])-> str:
    print(f"\n user: {special_context.context},\n Agent:{agent.name}\n")
    return f"You are a math expert. User: {special_context.context.name}, Agent: {agent.name}. Please assist with math-related queries."

math_agent : Agent = Agent(name="Genius",instructions=special_prompt,model=llm_provider,tools=[search])

async def call_agent():
    user_context = UserInfo("mohamil",122)
    output = await Runner.run(
        starting_agent= math_agent,
        input="search for the best math tutor in my area" ,
        context=user_context )
    print(f"\n\n Output: {output.final_output}\n\n")


asyncio.run(call_agent())    

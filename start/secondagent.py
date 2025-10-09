#  0. Importing the necessary libraries
from agents import Agent, Runner, OpenAIChatCompletionsModel,function_tool, AsyncOpenAI,set_tracing_disabled
import os
import asyncio
from dotenv import load_dotenv, find_dotenv
set_tracing_disabled(disabled=True)

# 0.1. Loading the environment variables
load_dotenv(find_dotenv())

# 1. Which LLM Provider to use? -> Google Chat Completions API Service
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)




# 2. Which LLM Model to use?
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

# tools 

# @function_tool
# def multiply(a:int,b:int)-> int :
#     """ Exact Multiplication (use this instead of guessing math) """
#     return a*b
# @function_tool
# def sum(a:int, b:int) -> int :
#     """ Exact addition (use this instead of guessing math) """
#     return a+b
    
# creat  Agent
agent: Agent = Agent(
    name="Assistant",
    instructions=(
        'You are a helpful math assistant '
        ' Always follow DMAS rule (division, multiplication, addition, subtraction). '
        "Explain answers clearly and briefly for beginners."          
    ),
    model=llm_model)

# 4. Running the Agent

async def main():
    result =await Runner.run(starting_agent=agent, input="what is 4-4+8*9")

    print("AGENT RESPONSE: " , result.final_output)

asyncio.run(main())

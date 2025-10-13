import asyncio
import os

from agents import Agent,trace,AsyncOpenAI,OpenAIChatCompletionsModel,RunContextWrapper, Runner,set_tracing_disabled, function_tool
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
gemini_api_key: str | None = os.environ.get("GOOGLE_API_KEY")

set_tracing_disabled(disabled=False)
external_client: AsyncOpenAI = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

llm_provider : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model='gemini-2.5-flash', openai_client=external_client) 
    
spanish_Agent = Agent(name="Spanish translator",model=llm_provider, instructions="Translate the input text to Spanish.")
french_Agent = Agent(name="French translator",model=llm_provider, instructions="Translate the input text to French.")

# Create tools for each agent
spanish_Agent_tool = spanish_Agent.as_tool(
    #   this is metadata about the tool this will help 
           tool_name="translate_to_spanish",
           tool_description="Translate the user's message to Spanish.") , 

french_Agent_tool = french_Agent.as_tool(
    #  this is metadata about the tool
           tool_name="translate_to_french",
           tool_description="Translate the user's message to French.")

agent = Agent(
              name="Orchestration",
              model=llm_provider,
              tools=[spanish_Agent_tool, french_Agent_tool],
              instructions="Decide whether to translate the input text to Spanish or French based on the user's preference. Use the appropriate tool to perform the translation.",
           )


async def main():
    with trace("Translation workflow"): 
        result = await Runner.run(agent, "Translate 'Hello, how are you?' to French." )
        print(f"Final Output: {result.final_output}")


asyncio.run(main())
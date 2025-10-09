from agents import AsyncOpenAI,OpenAIChatCompletionsModel,RunContextWrapper, Runner,set_tracing_disabled, function_tool
from dotenv import load_dotenv, find_dotenv
import os
from agents import Agent, Runner, handoff
import asyncio


load_dotenv(find_dotenv())
gemini_api_key: str | None = os.environ.get("GOOGLE_API_KEY")

set_tracing_disabled(disabled=True)
external_client: AsyncOpenAI = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
llm_provider : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model='gemini-2.5-flash', openai_client=external_client) 

@function_tool
async def web_search(query: str) -> str:
    
    """Search the web for real-time information."""
    import requests
#  example using DuckDuckGo or Serper.dev
    response = requests.get(f"https://api.duckduckgo.com/?q={query}&format=json")
    data = response.json()
    return data["RelatedTopics"] or "No relevant results found."

triage_agent = Agent(
    name="searach engine",
    instructions=('You can answer questions or use the web_search tool for up-to-date info.'
      ),
    # tools= [web_search] ,
    model= llm_provider
)


async def main():
    result = await Runner.run(triage_agent, "who is current prisident of pakistan")
    print(result.final_output)

asyncio.run(main())

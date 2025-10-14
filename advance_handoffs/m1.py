from agents import AsyncOpenAI,OpenAIChatCompletionsModel, Runner,set_tracing_disabled
from dotenv import load_dotenv, find_dotenv
import os
from agents import Agent, Runner, handoff
import asyncio
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX



load_dotenv(find_dotenv())
gemini_api_key: str | None = os.environ.get("GOOGLE_API_KEY")

set_tracing_disabled(disabled=True)
external_client: AsyncOpenAI = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
llm_provider : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model='gemini-2.5-flash', openai_client=external_client) 




print(RECOMMENDED_PROMPT_PREFIX)
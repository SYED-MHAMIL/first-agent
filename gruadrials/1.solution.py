import asyncio
import os

from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel

from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    set_tracing_disabled ,
    AsyncOpenAI
    ,OpenAIChatCompletionsModel,
    TResponseInputItem,
    input_guardrail,
)



async def main():
    load_dotenv(find_dotenv())
    gemini_api_key: str | None = os.environ.get("GOOGLE_API_KEY")

    set_tracing_disabled(disabled=True)
    external_client: AsyncOpenAI = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
    llm_provider : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model='gemini-2.5-flash', openai_client=external_client)

    class MathHomeworkOutput(BaseModel):
        is_math_homework: bool
        reasoning: str
    

    
    

from agents import AsyncOpenAI,RunContextWrapper,handoff,OpenAIChatCompletionsModel, Runner,set_tracing_disabled, function_tool
from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv())
gemini_api_key: str | None = os.environ.get("GOOGLE_API_KEY")

set_tracing_disabled(disabled=True)
external_client: AsyncOpenAI = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
llm_provider : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model='gemini-2.5-flash', openai_client=external_client) 

def log_handoff_event(ctx: RunContextWrapper):
    print(f"HNADOFF INITIATED:  Transferring to the Escalation Agent at {ctx.current_timestamp_ms}")




custom_handoff = handoff(
      
)
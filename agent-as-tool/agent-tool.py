from agents import Agent,trace,AsyncOpenAI,OpenAIChatCompletionsModel,RunContextWrapper, Runner,set_tracing_disabled, function_tool
from dotenv import load_dotenv, find_dotenv
import asyncio
import os

load_dotenv(find_dotenv())
gemini_api_key: str | None = os.environ.get("GOOGLE_API_KEY")

set_tracing_disabled(disabled=True)

external_client: AsyncOpenAI = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
llm_provider : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model='gemini-2.5-flash', openai_client=external_client) 



proofreader = Agent(
    name="Proofreader",
    instructions="Fix grammar and punctuation. Keep meaning. Reply only with the corrected text."
    ,model=llm_provider
)

@function_tool
async def proofread_text(text: str) -> str:
    """Fix grammar and punctuation; return only corrected text."""
    result = await Runner.run(proofreader, text, max_turns=3)
    return str(result.final_output)

# Main agent that uses the proofreader as just another tool
teacher_agent = Agent(
    name="Teacher",
    instructions="Help students write clearly. Use tools when asked to fix text.",
    tools=[proofread_text],
    model= llm_provider 
)

async def main():
    # with trace("Proofreading workflow"): 
        result = await Runner.run(teacher_agent, "Please proofread this sentence: 'She dont know how to do it right'", max_turns=3)
        print(f"Final Output: {result.final_output}")


asyncio.run(main())

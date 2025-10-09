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

billing_agent = Agent(name="Billing agent", instructions="Handle billing questions." ,model= llm_provider)
refund_agent  = Agent(name="Refund agent",  instructions="Handle refunds.",model=llm_provider)

triage_agent = Agent(
    name="Triage agent",
    instructions=(
        "Help the user with their questions. "
        "If they ask about billing, handoff to the Billing agent. "
        "If they ask about refunds, handoff to the Refund agent."
    ),
    handoffs=[billing_agent, handoff(refund_agent)],  # either direct agent or `handoff(...)`
    model= llm_provider
)


async def main():
    result = await Runner.run(triage_agent, "I need to check refund status.")
    print(result.final_output)

asyncio.run(main())

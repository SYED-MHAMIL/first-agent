from agents import AsyncOpenAI,RunContextWrapper,OpenAIChatCompletionsModel, Runner,set_tracing_disabled ,function_tool
from dotenv import load_dotenv, find_dotenv
from agents.extensions import handoff_filters
import os
from agents import Agent, Runner, handoff
import asyncio
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel


load_dotenv(find_dotenv())
gemini_api_key: str | None = os.environ.get("GOOGLE_API_KEY")

set_tracing_disabled(disabled=True)
external_client: AsyncOpenAI = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
llm_provider : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model='gemini-2.5-flash', openai_client=external_client) 


class HandoffData(BaseModel):
    summary: str

# --- Define our specialist agents ---
billing_agent = Agent(name="Billing Agent", instructions="Handle billing questions." ,model=llm_provider)
technical_agent = Agent(name="Technical Support Agent",model=llm_provider, instructions="Troubleshoot technical issues.")

# --- Define our on_handoff callback ---
def log_the_handoff(ctx: RunContextWrapper, input_data: HandoffData):
    print(f"\n[SYSTEM: Handoff initiated. Briefing: '{input_data.summary}']\n")



# --- TODO 1: Create the advanced handoffs ---

# Create a handoff to `billing_agent`.
# - Override the tool name to be "transfer_to_billing".
# - Use the `log_the_handoff` callback.
# - Require `HandoffData` as input.
to_billing_handoff = handoff(
    # Your code here
    agent= billing_agent,
    tool_name_override= "escalate_to_billing" ,
    tool_description_override="Use this for billing purpose",
    on_handoff=log_the_handoff,
    input_type= HandoffData
)

# Create a handoff to `technical_agent`.
# - Use the `log_the_handoff` callback.
# - Require `HandoffData` as input.
# - Add an input filter: `handoff_filters.remove_all_tools`.
to_technical_handoff = handoff(
    # Your code here
    agent= technical_agent ,
    on_handoff=log_the_handoff,
    input_type= HandoffData ,
    input_filter= handoff_filters.remove_all_tools

)

@function_tool
def diagnose():
    return "The user's payment failed."



# --- Triage Agent uses the handoffs ---
triage_agent = Agent(
    name="Triage Agent",
    instructions="First, use the 'diagnose' tool. Then, based on the issue, handoff to the correct specialist with a summary.",
    tools=[
        # A dummy tool for the triage agent to use
         diagnose 

    ],
    handoffs=[to_billing_handoff, to_technical_handoff],
    model= llm_provider
)


async def main():
    print("--- Running Scenario: Billing Issue ---")
    result = await Runner.run(triage_agent, "My payment won't go through.")
    print(f"Final Reply From: {result.last_agent.name}")
    print(f"Final Message: {result.final_output}")

asyncio.run(main())
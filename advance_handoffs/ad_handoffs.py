from agents import AsyncOpenAI,RunContextWrapper,Agent,handoff,OpenAIChatCompletionsModel, Runner,set_tracing_disabled, function_tool
from dotenv import load_dotenv, find_dotenv
from agents.extensions import handoff_filters

import os
import asyncio
from pydantic import BaseModel


load_dotenv(find_dotenv())
gemini_api_key: str | None = os.environ.get("GOOGLE_API_KEY")

set_tracing_disabled(disabled=True)
external_client: AsyncOpenAI = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
llm_provider : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model='gemini-2.5-flash', openai_client=external_client) 


def log_handoff_event(ctx: RunContextWrapper):
    print(f"HNADOFF INITIATED:  Transferring to the Escalation Agent at ")



class EscalationData(BaseModel):
    reason: str
    order_id: str

async def on_escalation(ctx: RunContextWrapper, input_data: EscalationData):
    print(f"Escalating order {input_data.order_id} because: {input_data.reason}")

specialist = Agent(name="Payment cleared", instructions="Clear the payment ", model=llm_provider)

custom_handoff = handoff(
      agent= specialist ,
      tool_name_override="cleared_payment" ,
      tool_description_override="Use this for complex issues that require a specialist.",
      on_handoff= on_escalation,  
      input_type=EscalationData, # The LLM must provide this data
       
)


faq_agent = Agent(name="FAQ agent" , model= llm_provider)

handoffs_faq  =  handoff(
      agent=  faq_agent,
      tool_name_override="given_faq" ,
      tool_description_override="faq_given",
      input_filter=  handoff_filters.remove_all_tools 
)


main_agent  = Agent(
    name="Triage Agent",
    instructions="assists user preference" ,
    model=llm_provider ,
    handoffs=[custom_handoff, handoffs_faq] 
    )


async def main():
 result =await Runner.run(main_agent,"My payment won't go through and give me FAQS.")
 print(result.final_output)


asyncio.run(main())
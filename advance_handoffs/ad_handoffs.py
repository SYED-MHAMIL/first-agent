from agents import AsyncOpenAI,RunContextWrapper,Agent,handoff,OpenAIChatCompletionsModel, Runner,set_tracing_disabled, function_tool
from dotenv import load_dotenv, find_dotenv
import os
import asyncio


load_dotenv(find_dotenv())
gemini_api_key: str | None = os.environ.get("GOOGLE_API_KEY")

set_tracing_disabled(disabled=True)
external_client: AsyncOpenAI = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
llm_provider : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model='gemini-2.5-flash', openai_client=external_client) 


def log_handoff_event(ctx: RunContextWrapper):
    print(f"HNADOFF INITIATED:  Transferring to the Escalation Agent at ")


specialist = Agent(name="Payment cleared Agent", instructions="Clear the payment ", model=llm_provider)

custom_handoff = handoff(
      agent= specialist ,
      tool_name_override="cleared_payment" ,
      tool_description_override="Use this for complex issues that require a specialist.",
      on_handoff=log_handoff_event,  
      
)


main_agent  = Agent(
    name="Triage Agent",
    instructions="you have to tranasfer  the money" ,
    model=llm_provider ,
    handoffs=[custom_handoff] , 
    
)


async def main():
 result =await Runner.run(main_agent,"My payment won't go through.")
 print(result.final_output)


asyncio.run(main())
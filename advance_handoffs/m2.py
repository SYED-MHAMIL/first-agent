from agents import AsyncOpenAI,HandoffInputData,RunContextWrapper,OpenAIChatCompletionsModel, Runner,set_tracing_disabled ,function_tool
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



def summarized_news_transfer(data: HandoffInputData) -> HandoffInputData:
    print("\n\n[HANDOFF] Summarizing news transfer...\n\n")
    summarized_conversation = "Get latest tech news."
    
    return HandoffInputData(
        input_history=summarized_conversation,
        pre_handoff_items=(),
        new_items=(),
    )


@function_tool
def get_weather(city: str) -> str:
    """A simple function to get the weather for a user."""
    return f"The weather for {city} is sunny."

news_agent: Agent = Agent(
    name="NewsAgent",
    instructions="You get latest news about tech community and share it with me. Always transfer back to WeatherAgent after answering the questions",
    model=llm_provider,
)

planner_agent: Agent = Agent(
    name="PlannerAgent",
    instructions="You get latest news about tech community and share it with me. Always transfer back to WeatherAgent after answering the questions",
    model=llm_provider,
)

def news_region(region: str):
    def is_news_allowed(ctx: RunContextWrapper, agent: Agent) -> bool:
        return True if ctx.context.get("is_admin", False) and region == "us-east-1" else False
    return is_news_allowed

weather_agent: Agent = Agent(
    name="WeatherAgent",
    instructions=f"You are weather expert - share weather updates as I travel a lot. For all Tech and News let the NewsAgent handle that part by delegation. {RECOMMENDED_PROMPT_PREFIX}",
    model=llm_provider,
    handoffs=[handoff(agent=news_agent, is_enabled=news_region("us-east-1")), planner_agent]
)

res = Runner.run_sync(weather_agent, 
                      "Check if there's any news about OpenAI after GPT-5 launch - also what's the weather SF?", 
                      context={"is_admin": True}
                      )
                      
print("\nAGENT NAME", res.last_agent.name)
print("\n[RESPONSE:]", res.final_output)
print("\n[NEW_ITEMS:]", res.new_items)



from agents import Agent, Runner, AsyncOpenAI, set_default_openai_client, set_tracing_disabled, set_default_openai_api

gemini_api_key = ""
set_tracing_disabled(True)
set_default_openai_api("chat_completions")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
set_default_openai_client(external_client)

agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant", model="gemini-2.0-flash")
# so all agents runner will use same client if you have the like 10 agents unless you overide it
result = Runner.run_sync(agent, "Hello")

print(result.final_output)








# "******************************* ***********  
#                FOR EXAMPLE        
# **********************************************"


# Global default client (Gemini)
set_default_openai_client(external_client)

# Create a different client (maybe OpenAI)
from openai import AsyncOpenAI
openai_client = AsyncOpenAI(api_key="sk-...")

# Agent that uses Gemini (default)
agent_gemini = Agent(name="GeminiAgent", instructions="Using Gemini", model="gemini-2.0-flash")

# Agent that uses OpenAI explicitly
from agents import OpenAIChatCompletionsModel
model_openai = OpenAIChatCompletionsModel(model="gpt-4o-mini", openai_client=openai_client)
agent_openai = Agent(name="OpenAIAgent", instructions="Using OpenAI", model=model_openai)

import asyncio
import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent,Runner,set_default_openai_api,set_default_openai_client,set_tracing_export_api_key
from openinference.instrumentation.openai_agents import OpenAIAgentsInstrumentor
from openai import AsyncOpenAI 
from langfuse import get_client





# load  env
load_dotenv(find_dotenv())
gemini_api_key: str | None = os.environ.get("GOOGLE_API_KEY")
os.get("LANGFUSE_SECRET_KEY")
os.get("LANGFUSE_PUBLIC_KEY")
os.get("LANGFUSE_HOST")


external_client: AsyncOpenAI = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/") 
set_default_openai_client(external_client,use_for_tracing=False)
set_default_openai_api("chat_completions")


# get the logs and traces

OpenAIAgentsInstrumentor.instrument() 

# Verify connection

langfuse =  get_client()

if langfuse.auth_check():
    print("✅ Langfuse client is authenticated and ready!")
else:
    print("❌ Authentication failed. Please check your credentials and host.")
    


async def main():
    """Run an AI agent that replies in haikus."""
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model = "gemini-2.5-flash",
    )

    result = await Runner.run(agent, "Tell me about recursion in programming.")
    print("\n--- Agent Response ---")
    print(result.final_output)


# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    asyncio.run(main())
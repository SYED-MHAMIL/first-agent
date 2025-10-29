"""
------------------------------------------------------------
Async AI Agent Demo — Gemini with Langfuse Observability
------------------------------------------------------------
This script sets up an AI agent that communicates using haikus.
It integrates:
    - Google Gemini (via OpenAI-compatible endpoint)
    - Langfuse for observability and tracing
    - Async execution for scalability and performance

Author: [Your Name]
Date: [Date]
------------------------------------------------------------
"""

# -----------------------------
# Imports
# -----------------------------
import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI
from openinference.instrumentation.openai_agents import OpenAIAgentsInstrumentor
from langfuse import get_client, observe
from agents import (
    Agent,
    set_default_openai_key,
    Runner,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_export_api_key,
)

# -----------------------------
# 1. Load and configure environment
# -----------------------------

# Load environment variables from the nearest .env file
load_dotenv(find_dotenv())

# Initialize instrumentation for OpenAI Agents (for observability/tracing)
OpenAIAgentsInstrumentor().instrument()

# Fetch required environment variables
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST")

# Load API keys for Google Gemini and OpenAI
gemini_api_key = os.getenv("GOOGLE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

# -----------------------------
# 2. Configure the OpenAI client to use Gemini endpoint
# -----------------------------
# Note:
# Gemini supports an OpenAI-compatible API endpoint,
# so we can use the AsyncOpenAI client by setting base_url accordingly.

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Register this Gemini client as the default for your agents
set_default_openai_client(client=client, use_for_tracing=False)

# Set the default OpenAI API endpoint type (chat-based completions)
set_default_openai_api("chat_completions")

# Export tracing data using the OpenAI API key (used by Langfuse)
set_tracing_export_api_key(openai_api_key)

# -----------------------------
# 3. Initialize Langfuse client
# -----------------------------
langfuse = get_client()

# Check authentication
if langfuse.auth_check():
    print("✅ Langfuse client is authenticated and ready!")
else:
    print("❌ Authentication failed. Please check your credentials and host.")

# -----------------------------
# 4. Define the async main function
# -----------------------------
@observe()  # Langfuse decorator to automatically capture traces
async def main():
    """
    Main coroutine to run an AI agent that responds in haikus.
    Observability data is automatically captured via Langfuse.
    """
    
    # Define the user input
    input_text = "tell me about opwn ai. ?"

    # Create an agent with specific behavior instructions
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model="gemini-2.5-flash",
    )

    # Execute the agent’s reasoning and capture results
    result = await Runner.run(agent, input_text)

    # Extract the final AI response
    output = result.final_output

    # Add rich metadata and context to the current Langfuse trace
    langfuse.update_current_trace(
        input=input_text,
        output=output,
        user_id="user_gemini_001",
        session_id="session_haiku_demo",
        tags=["agent", "haiku", "gemini", "recursion"],
        metadata={
            "model": "gemini-2.5-flash",
            "agent_type": "haiku_generator",
            "topic": "recursion"
        },
        version="1.0.0"
    )

    # Display the agent’s response
    print("\n--- Agent Response ---")
    print(output)

    return output

# -----------------------------
# 5. Script Entry Point
# -----------------------------
if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())

    # Flush Langfuse events to ensure all telemetry is sent
    langfuse.flush()

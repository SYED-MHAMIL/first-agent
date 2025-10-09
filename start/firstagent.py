from agents import Agent, Runner, AsyncOpenAI, function_tool, set_default_openai_client, set_tracing_disabled,OpenAIChatCompletionsModel , set_default_openai_api
import os
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")
set_tracing_disabled(disabled=True)
# set_default_openai_api("chat_completions")
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

## you CAn not use dirctly gimini ai  
# so Your ask gimini function will never run 




@function_tool
def ask_gemini(prompt: str) -> str:
    """Ask Google Gemini API for a response."""
    response = model.generate_content(prompt)
    return response.text

@function_tool
def mul(num1: int,num2:int) -> str:
    """Multiplication of two  number"""
    return f"The multiplicaation of {num1 *num2}"




external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"   
)

agent: Agent = Agent(
    name="Assistant",
      instructions="You are a helpful assistant",
      model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=external_client),
      tools=[ask_gemini,] )

# result = Runner.run_sync(agent, "What's wheather of tokya")

# print(result.final_output)


import json 
print(agent.tools)
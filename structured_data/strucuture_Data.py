import asyncio
import os
from pydantic import  BaseModel
from agents import Agent,ItemHelpers,AsyncOpenAI,OpenAIChatCompletionsModel,RunContextWrapper, Runner,set_tracing_disabled, function_tool
from dotenv import load_dotenv, find_dotenv


async def main():
    load_dotenv(find_dotenv())
    gemini_api_key: str | None = os.environ.get("GOOGLE_API_KEY")

    set_tracing_disabled(disabled=True)
    external_client: AsyncOpenAI = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
    llm_provider : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model='gemini-2.5-flash', openai_client=external_client) 
    
    class PersonInfo(BaseModel):
            name: str
            age: int
            occupation: str
            
    
    agent = Agent(
    name="InfoCollector",
    instructions="Extract person information from the user's message.",
    output_type=PersonInfo  # This is the magic!
    , model= llm_provider
    )

    # Test it
    result =await Runner.run(
        agent, 
        "Hi, I'm Alice, I'm 25 years old and I work as a teacher."
        ,
    )

# Now you get perfect structured data!
    print("Type:", type(result.final_output))        # <class 'PersonInfo'>
    print("Name:", result.final_output.name)         # "Alice"
    print("Age:", result.final_output.age)           # 25
    print("Job:", result.final_output.occupation)    # "teacher"
    print("data", result)


if __name__  == "__main__":
    asyncio.run(main())


import asyncio
from dataclasses import dataclass
import os

from agents import Agent,AgentHooks, ModelSettings ,ItemHelpers,AsyncOpenAI,OpenAIChatCompletionsModel,RunContextWrapper, Runner,set_tracing_disabled, function_tool
from dotenv import load_dotenv, find_dotenv
from openai.types.responses import ResponseTextDeltaEvent


async def main():
    load_dotenv(find_dotenv())
    gemini_api_key: str | None = os.environ.get("GOOGLE_API_KEY")

    set_tracing_disabled(disabled=True)
    external_client: AsyncOpenAI = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
    llm_provider : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model='gemini-2.5-flash', openai_client=external_client) 
    import random
    @function_tool
    def how_many_jokes():
        return random.randint(1, 10)

    
    @function_tool
    def calculate_area(length: float, width: float) -> str:
        return f"Area = {length * width} square units"

    @function_tool
    def get_weather(city: str) -> str:
        return f"Weather in {city}: Sunny, 72°F"
    
    @function_tool
    def new_tool():
        return "I'm a new tool"
    

    class MyAgentHooks(AgentHooks):
        async def on_start(self, context, agent):
            print(f"🕘 {agent.name} is starting up!")
    
        async def on_llm_start(self, context, agent, system_prompt, input_items):
            print(f"📞 {agent.name} is asking AI for help")
        
        async def on_llm_end(self, context, agent, response):
            print(f"🧠✨ {agent.name} got AI response")
        
        async def on_tool_start(self, context, agent, tool):
            print(f"🔨 {agent.name} is using {tool.name}")
        
        async def on_tool_end(self, context, agent, tool, result):
            print(f"✅ {agent.name} finished using {tool.name}")
        
        async def on_end(self, context, agent, output):
            print(f"🎉 {agent.name} completed the task!")

# Create an agent
    my_agent = Agent(
        name="Helper Bot",
        instructions= "you are heelpfll agent" ,
        model= llm_provider ,
        tools= [get_weather,calculate_area], 
        hooks = MyAgentHooks()
    )

    # Attach our hooks to this specific agent
    result =await Runner.run(my_agent , "what is the karachi wheather")
    print("output" , result.final_output)




asyncio.run(main())
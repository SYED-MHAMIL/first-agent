import asyncio
from dataclasses import dataclass
import os

from agents import Agent, ModelSettings ,ItemHelpers,AsyncOpenAI,OpenAIChatCompletionsModel,RunContextWrapper, Runner,set_tracing_disabled, function_tool
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

    print("Clonning agent question\n")

    # agent = Agent(
    # name="Joker",
    # instructions=  "You tell me first jokes",
    # model= llm_provider , 
    #  tools= [how_many_jokes]
    #  )
    
    # result = Runner.run_streamed(agent,input= "Please tell me 5 jokes.")
    # async for event in result.stream_events():
    #     if event.type == "raw_response_event" and isinstance(event.data,ResponseTextDeltaEvent):   
    #        print(event.data.delta, end="", flush=True)

    
    # print("*"*30)
    # print("Run item events and agent event:\n")
    



    # agent1 = agent.clone(
    # name="Joker",
    # instructions=  "You are a helpful assistant. First, determine how many jokes to tell, then provide jokes.",
    #  )
    
    # result = Runner.run_streamed(agent1,input=  " Hello ")
    # async for event in result.stream_events():
    #      # We'll ignore the raw responses event deltas
    #     if event.type == "raw_response_event":
    #         continue
    #     # When the agent updates, print that
    #     elif event.type == "agent_updated_stream_event":
    #         print(f"Agent updated: {event.new_agent.name}")
    #         continue
    #     # When items are generated, print them
    #     elif event.type == "run_item_stream_event":
    #         if event.item.type == "tool_call_item":
    #             print("-- Tool was called")
    #         elif event.item.type == "tool_call_output_item":
    #             print(f"-- Tool output: {event.item.output}")
    #         elif event.item.type == "message_output_item":
    #             print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
    #         else:
    #             pass  # Ignore other event types


    base_agent = Agent(
    name="BaseAssistant",
    instructions="You are a helpful assistant.",
    model_settings=ModelSettings(temperature=0.7)
    ,model=llm_provider , 
    tools=[calculate_area]

    )
    
    friendly_agent = base_agent.clone(
    name="FriendlyAssistant",
    instructions="You are a very friendly and warm assistant."
    )
# wheather  agent copy from base  
    weather_agent   = base_agent.clone(
    name="WeatherAssistant",
    instructions="You are a weather and math  assistant." ,
    tools=[calculate_area,get_weather]
    )
    
    
    math_agent = base_agent.clone(
    name="MathAssistant",
    tools=[calculate_area],  # Same tools
    instructions="You are a math specialist."
)
    base_agent.tools.append(new_tool)

    print("friendly tool",friendly_agent.tools) 
    print("Weather tool",weather_agent.tools) 
    print("Weather tool",math_agent.tools) 
   
    
    query =  "hello, How are You"
    result  =await Runner.run(base_agent, query )
    result1  =await Runner.run(friendly_agent, query)
    result_wheather  =await Runner.run(weather_agent, "whather of karachi")
    result_math  =await Runner.run(math_agent, query)

    print(" help full asistannt \n")
    # print(result.final_output)

    print("frifndly full asistannt \n")
    # print(result1.final_output)
     

    print("Wheather asistannt \n")
    # print(result_wheather.final_output)
    


    print("Math agent asistannt \n")
    # print(result_math.final_output)


    print("\n ONE all Exmaplples \n")
    print("*" * 30)
  

    # Create a base agent
    base_agent = Agent(
        name="BaseAssistant",
        instructions="You are a helpful assistant.",
        model_settings=ModelSettings(temperature=0.7),
        model= llm_provider
    )

    # Create multiple specialized variants
    agents = {
        "Creative": base_agent.clone(
            name="CreativeWriter",
            instructions="You are a creative writer. Use vivid language.",
            model_settings=ModelSettings(temperature=0.9)
        ),
        "Precise": base_agent.clone(
            name="PreciseAssistant", 
            instructions="You are a precise assistant. Be accurate and concise.",
            model_settings=ModelSettings(temperature=0.1)
        ),
        "Friendly": base_agent.clone(
            name="FriendlyAssistant",
            instructions=   "You are a very friendly assistant. Be warm and encouraging."
        ),
        "Professional": base_agent.clone(
            name="ProfessionalAssistant",
            instructions="You are a professional assistant. Be formal and business-like."
        )
    }

    # Test all variants
    query = "What is love"
    for name, agent in agents.items():
        result =await Runner.run(agent, query)
        print(f"\n{name} Agent:")
        print(result.final_output[:100] + "...")



    print("=== Run complete ===")


    print("\n🎉 You've learned streaming!")
    print("💡 Try changing the functions and see what happens!")





if __name__  == "__main__":
    asyncio.run(main())

import asyncio
import os

from agents import Agent ,ItemHelpers,AsyncOpenAI,OpenAIChatCompletionsModel,RunContextWrapper, Runner,set_tracing_disabled, function_tool
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




    print("Raw response events\n")

    # agent = Agent(
    # name="Joker",
    # instructions=  "You are a helpful assistant. First, determine how many jokes to tell, then provide jokes.",
    # model= llm_provider , 
    #  tools= [how_many_jokes]
    #  )
    
    # result = Runner.run_streamed(agent,input= "Please tell me 5 jokes.")
    # async for event in result.stream_events():
    #     if event.type == "raw_response_event" and isinstance(event.data,ResponseTextDeltaEvent):   
    #        print(event.data.delta, end="", flush=True)

    
    print("*"*30)
    print("Run item events and agent event:\n")
    

    agent = Agent(
    name="Joker",
    instructions=  "You are a helpful assistant. First, determine how many jokes to tell, then provide jokes.",
    model= llm_provider , 
     tools= [how_many_jokes]
     )
    
    result = Runner.run_streamed(agent,input=  " Hello ")
    async for event in result.stream_events():
         # We'll ignore the raw responses event deltas
        if event.type == "raw_response_event":
            continue
        # When the agent updates, print that
        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
            continue
        # When items are generated, print them
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
            else:
                pass  # Ignore other event types

    print("=== Run complete ===")






    print("\n🎉 You've learned streaming!")
    print("💡 Try changing the functions and see what happens!")





if __name__  == "__main__":
    asyncio.run(main())
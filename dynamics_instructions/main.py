import asyncio
from dataclasses import dataclass
import os

from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,RunContextWrapper, Runner,set_tracing_disabled, function_tool
from dotenv import load_dotenv, find_dotenv


def main():
    load_dotenv(find_dotenv())
    gemini_api_key: str | None = os.environ.get("GOOGLE_API_KEY")

    set_tracing_disabled(disabled=True)
    external_client: AsyncOpenAI = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
    llm_provider : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model='gemini-2.5-flash', openai_client=external_client) 

    @dataclass
    class UserInfo:  
        name: str
        uid: int

    user_info = UserInfo("zain",1) 
    
  # 🎯 Example 1: Basic Dynamic Instructions
    print("\n🎭 Example 1: Basic Dynamic Instructions")
    print("-" * 40)

    def basic_dynamic(context: RunContextWrapper[UserInfo], agent: Agent) -> str:
        """Basic dynamic instructions function."""
        return f"You are {agent.name}. Be helpful and friendly."
    
    agent_basic = Agent(
        name="Dynamic Agent",
        instructions=basic_dynamic,
        model=llm_provider
    )
    
    result = Runner.run_sync(agent_basic, "Hello!", context=user_info)
    print("Basic Dynamic Agent:")
    print(result.final_output)


    
    # 🎯 Example 2: Context-Aware Instructions
    print("\n🎭 Example 2: dynamic_instructions  Instructions")
    print("-" * 40)

    def dynamic_instructions(context: RunContextWrapper[UserInfo], agent: Agent) -> str:
        return f"You are {agent.name}. Adapt to the user's needs. The user's name is {context.context.name}. Help them with their questions."


    agent = Agent(
        name="Smart Assistant",
        instructions=dynamic_instructions , # ✅ Changes based on context
        model=llm_provider
    )

    user_info = UserInfo("zain",1)

    output = Runner.run_sync(agent,input= "what is user name",context=user_info)
    print(output.final_output)


    # 🎯 Example 3: Context-Aware Instructions
    print("\n🎭 Example 3: Context-Aware Instructions")
    print("-" * 40)
    def context_aware(context:RunContextWrapper[UserInfo],agent:Agent):
        """Context-aware instructions based on message count."""
        message_count = len(getattr(context, 'messages', []))
        
        if message_count == 0:
            return "You are a welcoming assistant. Introduce yourself!"
        elif message_count < 3:
            return "You are a helpful assistant. Be encouraging and detailed."
        else:
            return "You are an experienced assistant. Be concise but thorough."
    
    agent_context = Agent(
        name="Context Aware Agent",
        instructions=context_aware,
        model=llm_provider
    )    

    # result1= Runner.run_sync(agent_context,"hello",context=user_info)
    # print("First message:")
    # print(result1.final_output)
    
    # result2 = Runner.run_sync(agent_context, "Tell me about Python",context=user_info)
    # print("\nSecond message:")
    # print(result2.final_output)
    
    
    # 🎯 Example 3: Time-Based Instructions
    print("\n🎭 Example 4: Time-Based Instructions")
    print("-" * 40)
    
    import datetime
    
    def time_based(context: RunContextWrapper[UserInfo], agent: Agent) -> str:
        """Time-based instructions based on current hour."""
        current_hour = datetime.datetime.now().hour
        if 6<=current_hour < 12:
            return f"You are {agent.name}. Good morning! Be energetic and positive."
        elif 12 <= current_hour < 17:
            return f"You are {agent.name}. Good afternoon! Be focused and productive."
        else:
            return f"You are {agent.name}. Good evening! Be calm and helpful."
    
    agent_time_based = Agent(
        name="Context Aware Agent",
        instructions=time_based,
        model=llm_provider
    )    

    # result1= Runner.run_sync(agent_time_based,"hello",context=user_info)
    print("First message:")
    # print(result1.final_output)
    
    
    
    # 🎯 Example 4: Stateful Instructions (Remembers)
    print("\n🎭 Example 5: Stateful Instructions")
    print("-" * 40)
    
    class StatefulInstruction:
        """Stateful instructions that remember interaction count."""
        def __init__(self):
            self.interaction_count = 0
        
        def __call__(self, context: RunContextWrapper, agent: Agent) -> str:
            self.interaction_count += 1
            
            if self.interaction_count == 1:
                return "You are a learning assistant. This is our first interaction - be welcoming!"
            elif self.interaction_count <= 3:
                return f"You are a learning assistant. This is interaction #{self.interaction_count} - build on our conversation."
            else:
                return f"You are an experienced assistant. We've had {self.interaction_count} interactions - be efficient."
    
    instruction_gen = StatefulInstruction()
    agent_stateful = Agent(
        name= "StateFul agent", 
        instructions=instruction_gen,
        model= llm_provider
    )

    # for i in range(3):
    #     result = Runner.run_sync(agent_stateful,input=f"Question {i+1}: Tell me about AI",context=user_info)
    #     print(f"Interaction {i+1}:")
    #     print(result.final_output[:100] + "...")
    #     print()

      

     
     
    # 🎯 Example 5: Exploring Context and Agent
    print("\n🎭 Example 5: Exploring Context and Agent")
    print("-" * 40)
    
    def explore_context_and_agent(context: RunContextWrapper[UserInfo], agent: Agent) -> str:
        """Explore what's available in context and agent."""
        # Access conversation messages
        messages = getattr(context, 'messages', [])
        message_count = len(messages)
        
        # Access agent properties
        agent_name = agent.name
        tool_count = len(agent.tools)
        
        return f"""You are {agent_name} with {tool_count} tools. 
        This is message #{message_count} in our conversation.
        Be helpful and informative about ai tech stack!"""
    
    agent_explorer = Agent(
        name="Ai Assists",
        instructions=explore_context_and_agent,
        model=llm_provider
    )
    
    result = Runner.run_sync(agent_explorer, "What can you tell me about yourself?",context=user_info)
    print("Context Explorer Agent:")
    print(result.final_output)
    
    


    # 🎯 Example 5: Exploring Context and Agent
    print("\n🎭 Example 5: Async Dynamic Instructions")
    print("-" * 40)
    


    import asyncio

    async def asyncInstructions(context: RunContextWrapper[UserInfo],agent:Agent)->str:
        # Simulate Fetching data from database
        await asyncio.sleep(0.1)
        import datetime
        current_time = datetime.datetime.now().hour
        
        return f"""You are {agent.name}, an AI assistant with real-time capabilities.
                 Provide helpful and timely responses."""

    agent = Agent(
    name="Async Agent",
    instructions=asyncInstructions
    ,model= llm_provider

     )
    
     
    result = Runner.run_sync(agent, "What is ai-info?",context=user_info)
    print("Context Explorer Agent:")
    print(result.final_output)
    

    print("\n🎉 You've learned Dynamic Instructions!")
    print("💡 Try changing the functions and see what happens!")





if __name__  == "__main__":
    main()
# import os
import asyncio
# from dotenv import load_dotenv, find_dotenv
# from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, RunContextWrapper
# from agents.tool_context import ToolContext
# from dataclasses import dataclass
# from mem0 import MemoryClient

# @dataclass
# class UserContext:
#     username: str


# _: bool = load_dotenv(find_dotenv())

# set_tracing_disabled(True)

# # # ONLY FOR TRACING
# # os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

# gemini_api_key: str = os.getenv("GOOGLE_API_KEY", "")
# mem_mem0_api_key = os.getenv("MEM0_API_KEY", "")
# mem_client = MemoryClient(api_key= mem_mem0_api_key)
# # 1. Which LLM Service?
# external_client: AsyncOpenAI = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )


# llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
#     model="gemini-2.5-flash",
#     openai_client=external_client
# )





# @function_tool
# async def search_user_memory(context: ToolContext[UserContext], query: str):
#     return await asyncio.to_thread(
#         mem_client.search, query=query, user_id=context.context.username, top_k=3
#     )
# @function_tool 
# async def save_user_memory(context: ToolContext[UserContext], query: str):
#     """Use this tool to save user memories."""
#     response =await asyncio.to_thread(mem_client.add,query =query, user_id=context.context.username, top_k=3 )
#     return response

# def dynamic_instructions_generator(context: RunContextWrapper[UserContext], agent: Agent[UserContext]) -> str:
#     response = mem_client.search(query="General Behavior", user_id=context.context.username, top_k=3)
#     print(response)
#     return f"""Helpful Agent that can answer questions. 
#             Use search_user_memory to find information and save_user_memory to remember information.
#             User Past Memories: {response}
#             """


# orchestrator_agent: Agent = Agent(
#     name="DeepAgent",
#     instructions=dynamic_instructions_generator,
#     model=llm_model,
#     tools=[save_user_memory, search_user_memory],
# )

# while True:
#     # Part 1 Requirement Gathering
#     input_text = input("\n [User:] ")
#     if input_text.lower() in ["exit", "quit"]:
#         break
#     res = Runner.run_sync(orchestrator_agent, input_text, context=UserContext(username="muhammad"))
#     print( "\n [AGENT:]" , res.final_output) # requirement_completed, question






















import os

from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, RunContextWrapper
from agents.tool_context import ToolContext
from dataclasses import dataclass
from mem0 import MemoryClient

@dataclass
class UserContext:
    username: str

_: bool = load_dotenv(find_dotenv())

set_tracing_disabled(True)

# ONLY FOR TRACING
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

gemini_api_key: str = os.getenv("GOOGLE_API_KEY", "")

mem_client = MemoryClient()

# 1. Which LLM Service?
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

@function_tool
async def search_user_memory(context, query: str):
    return await asyncio.to_thread(
        mem_client.search, query=query, filters={"user_id": context.context.username}, top_k=3
    )
@function_tool
async def save_user_memory(context: ToolContext[UserContext], query: str):
    """Use this tool to save user memories."""
    response = await asyncio.to_thread(
        mem_client.add,
        [{"role": "user", "content": query}],
        user_id=context.context.username,
    )
    return response
async def dynamic_instructions_generator(context: RunContextWrapper[UserContext], agent: Agent[UserContext]) -> str:
    response = await asyncio.to_thread(
    mem_client.search,
    query="General Behavior",
    filters={"user_id": context.context.username},
    top_k=3,
)

    print(response)
    return f"""Helpful Agent that can answer questions. 
            Use search_user_memory to find information and save_user_memory to remember information.
            User Past Memories: {response}
            """
    

orchestrator_agent: Agent = Agent(
    name="DeepAgent",
    instructions=dynamic_instructions_generator,
    model=llm_model,
    tools=[save_user_memory, search_user_memory],
)

while True:
    # Part 1 Requirement Gathering
    input_text = input("\n [User:] ")
    if input_text.lower() in ["exit", "quit"]:
        break
    res = Runner.run_sync(orchestrator_agent, input_text, context=UserContext(username="muhammad"))
    print( "\n [AGENT:]" , res.final_output) # requirement_completed, question
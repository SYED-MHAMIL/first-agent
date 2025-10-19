import os

from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, RunContextWrapper
from agents.tool_context import ToolContext
from dataclasses import dataclass
from mem0 import MemoryClient
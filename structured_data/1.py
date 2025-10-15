from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
import os

from agents import Agent,ItemHelpers,AsyncOpenAI,OpenAIChatCompletionsModel,RunContextWrapper, Runner,set_tracing_disabled, function_tool
from dotenv import load_dotenv, find_dotenv
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv(find_dotenv())
gemini_api_key: str | None = os.environ.get("GOOGLE_API_KEY")

set_tracing_disabled(disabled=True)
external_client: AsyncOpenAI = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
llm_provider : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model='gemini-2.5-flash', openai_client=external_client) 

class ProductInfo(BaseModel):
    name: str                           # Text
    price: float                        # Decimal number
    in_stock: bool                      # True/False
    categories: List[str]               # List of text items
    discount_percent: Optional[int] = 0 # Optional number, default 0
    reviews_count: int                  # Whole number

# Create product info extractor
agent = Agent(
    name="ProductExtractor",
    instructions="Extract product information from product descriptions.",
    output_type=ProductInfo
    , model = llm_provider

)

# Test with product description
result = Runner.run_sync(
    agent,
    "The iPhone 15 Pro costs $999.99, it's available in electronics and smartphones categories, currently in stock with 1,247 reviews."

)

print("Product:", result.final_output.name)         # "iPhone 15 Pro"
print("Price:", result.final_output.price)          # 999.99
print("In Stock:", result.final_output.in_stock)    # True
print("Categories:", result.final_output.categories) # ["electronics", "smartphones"]
print("Reviews:", result.final_output.reviews_count) # 1247



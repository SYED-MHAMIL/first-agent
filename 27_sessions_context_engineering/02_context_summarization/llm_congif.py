import os   
from  openai import AsyncOpenAI
from agents import Agent ,OpenAIChatCompletionsModel,set_tracing_disabled
from dotenv import  load_dotenv


load_dotenv()

#  ============================================================ 

def set_gimini_model():
    set_tracing_disabled(disabled=True)
    """Configure gimini model using openAI-compatible API"""
    api_key  = os.getenv("GOOGLE_API_KEY")
    external_client = AsyncOpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
    
    return  OpenAIChatCompletionsModel(
         model="gemini-2.5-flash",
         openai_client= external_client   
    )   

llm_model  = set_gimini_model()
base_agent = Agent(
        name =  "Base Agent", 
        model = llm_model
)

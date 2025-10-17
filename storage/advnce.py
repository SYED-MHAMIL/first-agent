import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner , set_tracing_disabled ,SQLiteSession, OpenAIChatCompletionsModel, AsyncOpenAI

# 🌿 Load environment variables
load_dotenv(find_dotenv())
set_tracing_disabled(True)
# 🔐 Setup Gemini client
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

external_client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)
model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)

# Temporary memory (lost when program ends)
temp_session = SQLiteSession("temp_conversation")
set_tracing_disabled(disabled= True)
# Persistent memory (saved to file)
persistent_session = SQLiteSession("user_123", "conversations.db")

agent = Agent(name="Assistant", instructions="You are helpful.", model=model)

# Use temporary session
result1 = Runner.run_sync(
    agent,
    "Remember: my favorite color is blue",
    session=temp_session
)

# Use persistent session
result2 = Runner.run_sync(
    agent,
    "Remember: my favorite color is blue",
    session=persistent_session
)



print("Both sessions now remember your favorite color!")
print("But only the persistent session will remember after restarting the program.")


print( "tepporay",result1.final_output )
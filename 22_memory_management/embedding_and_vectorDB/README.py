import os
from dotenv import load_dotenv, find_dotenv
import faiss
import google.generativeai as genai
import numpy as np


load_dotenv(find_dotenv())
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)




# 1. Set embeddings from OpenAI

texts = ["dog", "puppy", "car"]
embeddings  = [genai.embed_content(model="models/embedding-001", content=t)["embedding"] for t in texts]
dimentions = len(embeddings)
print(embeddings)




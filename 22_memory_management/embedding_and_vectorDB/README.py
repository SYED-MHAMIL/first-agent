import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import faiss
import numpy as np

load_dotenv(find_dotenv())
# 1. Get embeddings from OpenAI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = OpenAI(api_key=GOOGLE_API_KEY)

texts = ["dog", "puppy", "car"]
embeddings  = [client.embeddings.create(model='text-embedding-3-small' ,input=t) for t in texts]
dimentions = len(embeddings)
print(embeddings)
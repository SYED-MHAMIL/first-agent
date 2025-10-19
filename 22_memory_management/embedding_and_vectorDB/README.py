from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
import faiss
import numpy as np


load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client =  OpenAI(api_key=OPENAI_API_KEY)


# 1. Set embeddings from OpenAI

texts = ["dog", "puppy", "car"]
embeddings  = [client.embeddings.create(model="text-embedding-3-small", input=t).data[0].embedding  for t in texts]
dimentions = len(embeddings)
print(embeddings)

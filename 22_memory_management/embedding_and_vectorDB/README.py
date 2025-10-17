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








# from  gimini can be done




import google.generativeai as genai
import numpy as np
import faiss

genai.configure(api_key="YOUR_GEMINI_API_KEY")

texts = ["dog", "puppy", "car"]

# Get embeddings from Gemini
embeddings = [genai.embed_content(model="models/embedding-001", content=t)["embedding"] for t in texts]

dimension = len(embeddings[0])
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# Query
query = "cute puppy"
query_embedding = genai.embed_content(model="models/embedding-001", content=query)["embedding"]

D, I = index.search(np.array([query_embedding]), k=2)

print("Query:", query)
print("Closest matches:", [texts[i] for i in I[0]])







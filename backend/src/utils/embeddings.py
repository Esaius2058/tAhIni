import os
import cohere
import requests
from dotenv import load_dotenv

load_dotenv()

cohere_api = os.getenv("COHERE_KEY")

def generate_embedding(text: str) -> list[float]:
    co = cohere.Client(cohere_api)
    response = co.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type="search_document"
    )

    embedding = response.embeddings[0]
    print(f"Length: {len(embedding)}")
    print(embedding[:10])
    return embedding

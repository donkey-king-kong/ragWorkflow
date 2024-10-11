from openai import AzureOpenAI
import openai
import os
from dotenv import load_dotenv
import json

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
ENDPOINT = os.getenv("OPENAI_ENDPOINT")

# Getting response from model
def getResponse(chunks):
    openai.api_type = "azure"
    deploymentName = "text-embedding-ada-002"
    openai.api_key = API_KEY
    openai.azure_endpoint= ENDPOINT
    openai.api_version = "2023-05-15"

    embedding = openai.embeddings.create(
        input=chunks,
        model=deploymentName
    )
    
    # This stores the embedding as a string
    embedding = embedding.model_dump_json() # Response is now a string of dictionary containing the keys: data, model, object and usage
    embedding = json.loads(embedding) # This converts the string of dictionary to a dictionary

    # This returns the embedding in a list
    return embedding['data'][0]['embedding']
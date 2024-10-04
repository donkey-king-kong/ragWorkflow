from openai import AzureOpenAI
import openai
import os
from document_specific_chunk import markdown_chunk_text
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
ENDPOINT = os.getenv("OPENAI_ENDPOINT")
headers = {
    "Content-Type": "application/json",
    "api-key": os.getenv("OPENAI_API_KEY")
}

# Getting response from model
def getResponse(chunks):
    openai.api_type = "azure"
    deploymentName = "text-embedding-ada-002"
    openai.api_key = API_KEY
    openai.azure_endpoint = ENDPOINT
    openai.api_version = "2023-05-15"

    embedding = openai.embeddings.create(
        input=chunks,
        model=deploymentName
    )

    return embedding

print(getResponse("Hello World"))
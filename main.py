from openai import AzureOpenAI
import openai
import os
from document_specific_chunk import chunk_text
import os
from dotenv import load_dotenv

load_dotenv()

headers = {
    "Content-Type": "application/json",
    "api-key": os.getenv("OPENAI_API_KEY")
}

# Getting response from model
def getResponse(chunks):
    openai.api_type = "azure"
    deploymentName = "text-embedding-ada-002"
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.azure_endpoint= os.getenv("OpenAI_ENDPOINT")
    openai.api_version = "2023-05-15"

    embedding = openai.embeddings.create(
        model=deploymentName,
        input=chunks
    )

    return embedding

print(getResponse("Hello World"))


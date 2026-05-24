from fastapi import FastAPI
from pydantic import BaseModel

from openai import AzureOpenAI
from dotenv import load_dotenv

import os

from scripts.prompt_loader import load_prompt
from tools.azure_search_retriever import (
    retrieve_from_azure_search
)

# Load environment variables
load_dotenv()

# Azure OpenAI configuration
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-02-15-preview"
)

# Load prompt
system_prompt = load_prompt("v3")

# Create FastAPI app
app = FastAPI(
    title="Enterprise GenAIOps API"
)

# Request model
class ChatRequest(BaseModel):
    message: str

# Chat endpoint
@app.post("/chat")
def chat(request: ChatRequest):

    # Retrieve enterprise context
    retrieved_context = retrieve_from_azure_search(
        request.message
    )

    augmented_input = f"""
User Question:
{request.message}

Enterprise Knowledge Context:
{retrieved_context}
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": augmented_input
        }
    ]

    response = client.chat.completions.create(
        model=deployment,
        messages=messages
    )

    assistant_reply = (
        response.choices[0].message.content
    )

    return {
        "user_question": request.message,
        "retrieved_context": retrieved_context,
        "assistant_response": assistant_reply
    }
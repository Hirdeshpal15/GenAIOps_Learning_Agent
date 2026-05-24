from openai import AzureOpenAI
from dotenv import load_dotenv

import os

from scripts.prompt_loader import load_prompt

from tools.azure_search_retriever import (
    retrieve_from_azure_search
)

# Load environment variables
load_dotenv()

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

print("=== Enterprise GenAIOps Agent ===")
print("Type 'exit' to quit.\n")

messages = [
    {"role": "system", "content": system_prompt}
]

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    # Retrieve Azure Search context
    retrieved_context = retrieve_from_azure_search(
        user_input
    )

    augmented_input = f"""
User Question:
{user_input}

Enterprise Knowledge Context:
{retrieved_context}
"""

    messages.append({
        "role": "user",
        "content": augmented_input
    })

    try:

        response = client.chat.completions.create(
            model=deployment,
            messages=messages
        )

        assistant_reply = (
            response.choices[0].message.content
        )

        messages.append({
            "role": "assistant",
            "content": assistant_reply
        })

        print("\nRetrieved Enterprise Context:\n")
        print(retrieved_context)

        print("\nAssistant:\n")
        print(assistant_reply)

        print("\n" + "-" * 50 + "\n")

    except Exception as e:

        print(f"\nError: {e}\n")
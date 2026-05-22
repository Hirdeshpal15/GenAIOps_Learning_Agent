from openai import AzureOpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Azure configuration
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Create Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-02-15-preview"
)

# Load system prompt
with open("prompts/system_prompt_v1.txt", "r", encoding="utf-8") as file:
    system_prompt = file.read()

print("=== GenAIOps Assistant V1 ===")
print("Type 'exit' to quit.\n")

# Conversation loop
while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )

        assistant_reply = response.choices[0].message.content

        print("\nAssistant:")
        print(assistant_reply)
        print("\n" + "-" * 50 + "\n")

    except Exception as e:
        print(f"Error: {e}")
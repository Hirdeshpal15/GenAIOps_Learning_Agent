from openai import AzureOpenAI
from dotenv import load_dotenv
import os
from datetime import datetime
from scripts.prompt_loader import load_prompt

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

# ----------- Select prompt version
PROMPT_VERSION = "v3"

# ----------- Load selected prompt
system_prompt = load_prompt(PROMPT_VERSION)

print(f"=== GenAIOps Assistant {PROMPT_VERSION.upper()} ===")
print("Type 'exit' to quit.\n")

# Conversation memory
messages = [
    {"role": "system", "content": system_prompt}
]

# Create log file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = f"logs/chat_{PROMPT_VERSION}_{timestamp}.txt"

# Conversation loop
while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    # Save user message
    messages.append(
        {"role": "user", "content": user_input}
    )

    try:
        # Send request
        response = client.chat.completions.create(
            model=deployment,
            messages=messages
        )

        assistant_reply = response.choices[0].message.content

        # Save assistant reply
        messages.append(
            {"role": "assistant", "content": assistant_reply}
        )

        print("\nAssistant:")
        print(assistant_reply)
        print("\n" + "-" * 50 + "\n")

        # Save logs
        with open(log_file, "a", encoding="utf-8") as log:
            log.write(f"USER: {user_input}\n")
            log.write(f"ASSISTANT: {assistant_reply}\n")
            log.write("-" * 50 + "\n")

    except Exception as e:
        error_message = str(e)

        print(f"\nError: {error_message}\n")

        with open(log_file, "a", encoding="utf-8") as log:
            log.write(f"ERROR: {error_message}\n")
            log.write("-" * 50 + "\n")
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

from scripts.prompt_loader import load_prompt

from tools.log_reader import read_latest_log
from tools.prompt_inspector import list_prompt_versions
from tools.evaluation_reader import read_latest_evaluation

# Load environment variables
load_dotenv()

# Azure configuration
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

print("=== GenAIOps Assistant V5 ===")
print("Type 'exit' to quit.\n")

messages = [
    {"role": "system", "content": system_prompt}
]

while True:

    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    # -----------------------------
    # Tool Routing
    # -----------------------------

    if "latest log" in user_input.lower():

        tool_result = read_latest_log()

        print("\n[TOOL OUTPUT]\n")
        print(tool_result)
        print("\n" + "-" * 50 + "\n")

        continue

    elif "prompt versions" in user_input.lower():

        tool_result = list_prompt_versions()

        print("\n[TOOL OUTPUT]\n")
        print(tool_result)
        print("\n" + "-" * 50 + "\n")

        continue

    elif "latest evaluation" in user_input.lower():

        tool_result = read_latest_evaluation()

        print("\n[TOOL OUTPUT]\n")
        print(tool_result)
        print("\n" + "-" * 50 + "\n")

        continue

    # -----------------------------
    # Normal LLM Conversation
    # -----------------------------

    messages.append(
        {"role": "user", "content": user_input}
    )

    try:

        response = client.chat.completions.create(
            model=deployment,
            messages=messages
        )

        assistant_reply = response.choices[0].message.content

        messages.append(
            {
                "role": "assistant",
                "content": assistant_reply
            }
        )

        print("\nAssistant:\n")
        print(assistant_reply)
        print("\n" + "-" * 50 + "\n")

    except Exception as e:

        print(f"\nError: {e}\n")
from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import json

from scripts.prompt_loader import load_prompt

from tools.tool_definitions import tool_definitions

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

print("=== GenAIOps Assistant V6 ===")
print("Type 'exit' to quit.\n")

messages = [
    {"role": "system", "content": system_prompt}
]

# Tool mapping
available_tools = {
    "read_latest_log": read_latest_log,
    "list_prompt_versions": list_prompt_versions,
    "read_latest_evaluation": read_latest_evaluation
}

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    messages.append(
        {"role": "user", "content": user_input}
    )

    try:

        # Initial model request
        response = client.chat.completions.create(
            model=deployment,
            messages=messages,
            tools=tool_definitions,
            tool_choice="auto"
        )

        response_message = response.choices[0].message

        # -----------------------------
        # Tool Calling
        # -----------------------------

        if response_message.tool_calls:

            for tool_call in response_message.tool_calls:

                tool_name = tool_call.function.name

                print(f"\n[TOOL CALLED]: {tool_name}\n")

                # Execute tool
                tool_function = available_tools[tool_name]

                tool_result = tool_function()

                # Add tool result to conversation
                messages.append(response_message)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result
                })

                # Second model request with tool output
                second_response = client.chat.completions.create(
                    model=deployment,
                    messages=messages
                )

                final_reply = second_response.choices[0].message.content

                print("\nAssistant:\n")
                print(final_reply)
                print("\n" + "-" * 50 + "\n")

        else:

            assistant_reply = response_message.content

            print("\nAssistant:\n")
            print(assistant_reply)
            print("\n" + "-" * 50 + "\n")

            messages.append({
                "role": "assistant",
                "content": assistant_reply
            })

    except Exception as e:

        print(f"\nError: {e}\n")
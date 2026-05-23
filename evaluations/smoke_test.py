from openai import AzureOpenAI
from dotenv import load_dotenv
import os

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

print("Running AI smoke test...")

response = client.chat.completions.create(
    model=deployment,
    messages=[
        {
            "role": "user",
            "content": "Say hello briefly."
        }
    ]
)

reply = response.choices[0].message.content

print("AI Response:")
print(reply)

# Very simple validation
if not reply or len(reply) < 2:
    raise Exception("Smoke test failed!")

print("Smoke test passed!")
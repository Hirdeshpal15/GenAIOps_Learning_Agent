from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import time
import json
from datetime import datetime

from evaluations.evaluation_dataset import evaluation_questions
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

# Prompt versions
prompt_versions = ["v1", "v2", "v3"]

# JSON log file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
json_log_file = f"logs/evaluation_json_{timestamp}.jsonl"

print("=== Running Structured Evaluation Logging ===\n")

# Run evaluations
for version in prompt_versions:

    print(f"\nEvaluating {version.upper()}...\n")

    system_prompt = load_prompt(version)

    for question in evaluation_questions:

        try:
            # Start timer
            start_time = time.time()

            response = client.chat.completions.create(
                model=deployment,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ]
            )

            # End timer
            end_time = time.time()

            latency = round(end_time - start_time, 2)

            assistant_reply = response.choices[0].message.content

            # Token metrics
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens

            # Structured telemetry object
            telemetry = {
                "timestamp": datetime.now().isoformat(),
                "prompt_version": version,
                "question": question,
                "latency_seconds": latency,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "response_preview": assistant_reply[:200]
            }

            # Print summary
            print(json.dumps(telemetry, indent=2))

            # Save JSON line
            with open(json_log_file, "a", encoding="utf-8") as log:
                log.write(json.dumps(telemetry) + "\n")

        except Exception as e:

            error_telemetry = {
                "timestamp": datetime.now().isoformat(),
                "prompt_version": version,
                "question": question,
                "error": str(e)
            }

            print(json.dumps(error_telemetry, indent=2))

            with open(json_log_file, "a", encoding="utf-8") as log:
                log.write(json.dumps(error_telemetry) + "\n")

print("\nStructured evaluation completed.")
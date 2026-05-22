from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import time
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

# Create log file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
evaluation_log = f"logs/evaluation_metrics_{timestamp}.txt"

print("=== Running Evaluation With Metrics ===\n")

# Run evaluations
for version in prompt_versions:

    print(f"\nEvaluating {version.upper()}...\n")

    system_prompt = load_prompt(version)

    with open(evaluation_log, "a", encoding="utf-8") as log:
        log.write(f"\n===== PROMPT {version.upper()} =====\n\n")

    for question in evaluation_questions:

        print(f"Question: {question}")

        try:
            # --------- Start timer
            start_time = time.time()

            response = client.chat.completions.create(
                model=deployment,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ]
            )

            # --------- End timer
            end_time = time.time()

            latency = round(end_time - start_time, 2)

            assistant_reply = response.choices[0].message.content

            # ---------  Token usage
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens

            print(f"Latency: {latency}s")
            print(f"Total Tokens: {total_tokens}")

            # ----------  Save results
            with open(evaluation_log, "a", encoding="utf-8") as log:

                log.write(f"QUESTION: {question}\n")
                log.write(f"LATENCY: {latency}s\n")
                log.write(f"PROMPT TOKENS: {prompt_tokens}\n")
                log.write(f"COMPLETION TOKENS: {completion_tokens}\n")
                log.write(f"TOTAL TOKENS: {total_tokens}\n")
                log.write(f"RESPONSE:\n{assistant_reply}\n")
                log.write("-" * 60 + "\n")

        except Exception as e:

            error_message = str(e)

            print(f"Error: {error_message}")

            with open(evaluation_log, "a", encoding="utf-8") as log:
                log.write(f"ERROR: {error_message}\n")
                log.write("-" * 60 + "\n")

print("\nEvaluation with metrics completed.")
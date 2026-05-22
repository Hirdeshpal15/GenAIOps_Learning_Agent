from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import time

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

from scripts.prompt_loader import load_prompt


# -----------  OpenTelemetry Setup

trace.set_tracer_provider(TracerProvider())

tracer = trace.get_tracer(__name__)

span_processor = SimpleSpanProcessor(ConsoleSpanExporter())

trace.get_tracer_provider().add_span_processor(span_processor)






# Load environment variables

load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")






# Azure OpenAI Client

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-02-15-preview"
)




# -----------------------------
# Traced Workflow
# -----------------------------

with tracer.start_as_current_span("genaiops-workflow"):

    # ------  Prompt loading span
    with tracer.start_as_current_span("load-prompt"):

        system_prompt = load_prompt("v2")

        time.sleep(1)

    # ------- Model call span
    with tracer.start_as_current_span("azure-openai-request"):

        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": "Explain tracing in GenAIOps simply."
                }
            ]
        )

        assistant_reply = response.choices[0].message.content

    # --------  Logging span
    with tracer.start_as_current_span("save-log"):

        with open("logs/trace_demo.txt", "a", encoding="utf-8") as log:

            log.write(assistant_reply + "\n")
            log.write("-" * 50 + "\n")

print("\nAssistant Response:\n")
print(assistant_reply)
from azure.monitor.opentelemetry import configure_azure_monitor

from opentelemetry import trace
from dotenv import load_dotenv

import os
import time

# Load environment variables
load_dotenv()


# Application Insights connection string
connection_string = os.getenv(
    "APPLICATIONINSIGHTS_CONNECTION_STRING"
)

# Configure Azure Monitor
configure_azure_monitor(
    connection_string=connection_string
)

# Create tracer
tracer = trace.get_tracer(__name__)

print("Sending telemetry to Azure Application Insights...\n")

# Example traced workflow
with tracer.start_as_current_span("genaiops-main-workflow"):

    with tracer.start_as_current_span("prompt-loading"):
        time.sleep(1)

    with tracer.start_as_current_span("model-request"):
        time.sleep(2)

    with tracer.start_as_current_span("evaluation-step"):
        time.sleep(1)

print("Telemetry sent successfully.")
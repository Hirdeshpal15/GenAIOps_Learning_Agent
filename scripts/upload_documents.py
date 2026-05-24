from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

service_name = os.getenv("AZURE_SEARCH_SERVICE")
admin_key = os.getenv("AZURE_SEARCH_KEY")

endpoint = f"https://{service_name}.search.windows.net"

# Create search client
credential = AzureKeyCredential(admin_key)

search_client = SearchClient(
    endpoint=endpoint,
    index_name="genaiops-index",
    credential=credential
)

# Example documents
documents = [

    {
        "id": "1",
        "content": """
GenAIOps combines AI engineering, MLOps,
monitoring, evaluations, observability,
and deployment automation.
"""
    },

    {
        "id": "2",
        "content": """
Azure Application Insights provides
telemetry, tracing, metrics, and
cloud observability features.
"""
    },

    {
        "id": "3",
        "content": """
Azure AI Search enables enterprise
retrieval systems for RAG applications.
"""
    }

]

# Upload documents
result = search_client.upload_documents(documents)

print("Documents uploaded successfully!")

print(result)
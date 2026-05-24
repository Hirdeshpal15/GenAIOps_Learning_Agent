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

# Query
query = "monitoring and telemetry"

print(f"\nSearching for: {query}\n")

results = search_client.search(
    search_text=query
)

# Display results
for result in results:

    print("Document ID:", result["id"])
    print("Content:")
    print(result["content"])

    print("\n" + "-" * 50 + "\n")
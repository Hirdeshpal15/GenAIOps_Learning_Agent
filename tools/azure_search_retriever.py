from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

service_name = os.getenv("AZURE_SEARCH_SERVICE")
admin_key = os.getenv("AZURE_SEARCH_KEY")

endpoint = f"https://{service_name}.search.windows.net"

# Search client
credential = AzureKeyCredential(admin_key)

search_client = SearchClient(
    endpoint=endpoint,
    index_name="genaiops-index",
    credential=credential
)

def retrieve_from_azure_search(query):

    results = search_client.search(
        search_text=query,
        top=3
    )

    retrieved_context = ""

    for result in results:

        retrieved_context += (
            f"\nDocument ID: {result['id']}\n"
        )

        retrieved_context += result["content"] + "\n"

    return retrieved_context
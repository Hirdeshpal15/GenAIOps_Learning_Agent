from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField
)

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

service_name = os.getenv("AZURE_SEARCH_SERVICE")
admin_key = os.getenv("AZURE_SEARCH_KEY")

endpoint = f"https://{service_name}.search.windows.net"

# Create index client
credential = AzureKeyCredential(admin_key)

index_client = SearchIndexClient(
    endpoint=endpoint,
    credential=credential
)

# Define index schema
fields = [
    SimpleField(name="id", type="Edm.String", key=True),

    SearchableField(
        name="content",
        type="Edm.String"
    )
]

# Create index
index = SearchIndex(
    name="genaiops-index",
    fields=fields
)

# Create in Azure
result = index_client.create_or_update_index(index)

print(f"Index created: {result.name}")
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Key Vault name
key_vault_name = os.getenv("KEY_VAULT_NAME")

# Build vault URL
kv_uri = f"https://{key_vault_name}.vault.azure.net"

print("Connecting to Key Vault...")
print("Vault URL:", kv_uri)

# Azure credential
credential = DefaultAzureCredential()

# Secret client
client = SecretClient(
    vault_url=kv_uri,
    credential=credential
)

# Retrieve secret
retrieved_secret = client.get_secret("openai-api-key")

print("\nSecret retrieved successfully!")
print("Secret length:", len(retrieved_secret.value))
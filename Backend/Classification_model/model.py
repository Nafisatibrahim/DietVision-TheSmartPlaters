from google.cloud import aiplatform
from google.oauth2 import service_account
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Retrieve variables
SERVICE_ACCOUNT_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")
ENDPOINT_ID = os.getenv("ENDPOINT_ID")

def test_vertex_connection():
    print("🔄 Initializing Vertex AI client...")

    # Authenticate with the service account
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_PATH)
    aiplatform.init(project=PROJECT_ID, location=REGION, credentials=credentials)

    print("✅ Connected to Vertex AI successfully.")

    # --- Fetch endpoint info ---
    print("Fetching list of endpoints...")
    endpoints = aiplatform.Endpoint.list()

    for ep in endpoints:
        print(f"📍 Endpoint: {ep.display_name} — {ep.resource_name}")

    # --- Retrieve your specific endpoint ---
    if ENDPOINT_ID:
        endpoint = aiplatform.Endpoint(endpoint_name=f"projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}")
        print(f"✅ Loaded endpoint successfully: {endpoint.display_name}")
    else:
        print("⚠️ ENDPOINT_ID not found in environment variables.")

if __name__ == "__main__":
    test_vertex_connection()

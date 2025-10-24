"""
Vertex AI Prediction Client
Handles image classification requests to Vertex AI endpoint.
"""

from google.cloud import aiplatform
from google.oauth2 import service_account
import streamlit as st
from dotenv import load_dotenv
import base64
import os
import json

# Load .env variables
load_dotenv()

SERVICE_ACCOUNT_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")
ENDPOINT_ID = os.getenv("ENDPOINT_ID")

# Authenticate once globally
# credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_PATH)
# aiplatform.init(project=PROJECT_ID, location=REGION, credentials=credentials)

if os.getenv("GOOGLE_APPLICATION_CREDENTIALS") and os.path.exists(os.getenv("GOOGLE_APPLICATION_CREDENTIALS")):
        credentials = service_account.Credentials.from_service_account_file(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
else:
        # Fallback for Streamlit Cloud

        credentials = service_account.Credentials.from_service_account_info(st.secrets["vertex"])

aiplatform.init(
        project=st.secrets["vertex"]["project_id"],
        location=st.secrets["vertex"]["REGION"],
        credentials=credentials
    )

# Create endpoint reference
endpoint = aiplatform.Endpoint(
    endpoint_name=f"projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}"
)

def predict_image_classification(image_path: str):
    """
    Sends an image file to the Vertex AI endpoint and returns predictions.
    """
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        # Convert image to base64
        encoded_image = base64.b64encode(image_bytes).decode("utf-8")

        # Prepare payload
        instance = {"content": encoded_image}
        instances = [instance]

        print("🔍 Sending image for prediction...")

        # Send request to Vertex AI
        prediction_response = endpoint.predict(instances=instances)
        predictions = prediction_response.predictions

        print("✅ Prediction successful!")
        return predictions

    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        return None


# Example test (run directly)
if __name__ == "__main__":
    test_image = "Backend\Classification_model\pizzaa.jpg"  # Replace with your local image
    results = predict_image_classification(test_image)
    print(json.dumps(results, indent=2))

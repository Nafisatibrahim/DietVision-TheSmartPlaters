"""
Upload & Analyze Page
Users can upload meal photos for AI-based food recognition and nutrition analysis.
"""

# Import libraries
import streamlit as st
from PIL import Image
import io

def show_upload_analyze_page(user):
    st.title("📸 Upload & Analyze Your Meal")

    if not user:
        st.warning("Please sign in to upload and analyze your meals.")
        return

    st.markdown("""
    ### 🥦 How it works
    1. Upload a photo of your meal.  
    2. Our AI model identifies the food and estimates its nutritional content.  
    3. You’ll see instant insights — calories, macronutrients, and more.
    """)

    # --- Upload section ---
    uploaded_file = st.file_uploader("📤 Upload your meal photo", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        # Display uploaded image preview
        image = Image.open(uploaded_file)
        st.image(image, caption="Your uploaded image", use_container_width=True)

        # Placeholder for AI analysis
        with st.spinner("🔍 Analyzing your meal..."):
            st.success("✅ Image uploaded successfully! AI analysis coming soon.")
            # Later: send to model for prediction or nutrition API
            # response = requests.post(API_URL, files={"file": uploaded_file})

    # --- Footer note ---
    st.markdown("---")
    st.info("💡 Tip: Use clear, well-lit food photos for better analysis accuracy.")





import streamlit as st
from PIL import Image
import io
import base64
from Backend.vertex_ai_client import predict_image

def show_upload_analyze_page(user):
    st.title("📸 Upload & Analyze Your Meal")

    if not user:
        st.warning("Please sign in to upload and analyze your meals.")
        return

    uploaded_file = st.file_uploader("📤 Upload your meal photo", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Your uploaded image", use_column_width=True)

        if st.button("🔍 Analyze with AI"):
            with st.spinner("Contacting Vertex AI..."):
                # Convert image to base64 / bytes
                image_bytes = uploaded_file.read()
                encoded_image = base64.b64encode(image_bytes)

                try:
                    response = predict_image(encoded_image)
                    prediction = response.predictions[0]
                    st.success("✅ Prediction received from Vertex AI!")
                    st.json(prediction)
                except Exception as e:
                    st.error(f"❌ Failed to get prediction: {e}")

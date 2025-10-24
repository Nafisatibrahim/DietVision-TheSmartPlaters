"""
Upload & Analyze Page
Send uploaded image to Vertex AI endpoint and display prediction.
"""

import streamlit as st
import tempfile
import json
from Backend.Classification_model.predictor import predict_image_classification

def show_upload_analyze_page():
    st.title("🍽️ Upload & Analyze Your Food")

    # Image upload widget
    uploaded_file = st.file_uploader("📸 Upload an image of your food", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Show preview
        st.image(uploaded_file, caption="Your uploaded image", use_column_width=True)

        if st.button("🔍 Analyze Food"):
            # Save temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                temp_file.write(uploaded_file.read())
                temp_path = temp_file.name

            with st.spinner("Sending image to AI model..."):
                result = predict_image_classification(temp_path)

            # Display results
            if result and isinstance(result, list) and len(result) > 0:
                preds = result[0]
                labels = preds.get("displayNames", [])
                scores = preds.get("confidences", [])

                if labels and scores:
                    top_idx = scores.index(max(scores))
                    food_name = labels[top_idx].replace("_", " ").title()
                    confidence = round(scores[top_idx] * 100, 2)

                    st.success(f"✅ Prediction: **{food_name}** ({confidence}% confidence)")
                    st.json(preds)  # optional: show all classes
                else:
                    st.warning("No predictions returned.")
            else:
                st.error("❌ Prediction failed or returned empty result.")

"""
Upload & Analyze Page
Users can upload meal photos for AI-based food recognition and nutrition analysis.
Send uploaded image to Vertex AI endpoint and display prediction.
"""

import streamlit as st
import tempfile
import json
from Backend.Classification_model.predictor import predict_image_classification

def show_upload_analyze_page(user):
    st.title("🍽️ Upload & Analyze Your Food")

    # Image upload widget
    uploaded_file = st.file_uploader("📸 Upload an image of your food", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Show preview
        st.image(uploaded_file, caption="Your uploaded image", use_container_width=True)

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

                    # st.success(f"✅ Prediction: **{food_name}** ({confidence}% confidence)") # show food name and confidence percententage
                    st.success(f"✅ Prediction: **{food_name}**")
                    # st.json(preds)  # show all classes

                    # Save to session_state so that chatbot or dashboard can access
                    st.session_state["last_prediction"] = {
                        "food_name": food_name,
                        "confidence": confidence,
                        "all_labels": labels,
                        "all_scores": scores
                    }

                    # Display result
                    st.markdown(f"""
                        <div style="
                            background-color: #fff8f0;
                            border-left: 6px solid #FF6F00;
                            border-radius: 10px;
                            padding: 1.2rem;
                            margin-top: 1rem;
                            box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                            <h3 style="margin:0;">🍕 Prediction: <b>{food_name}</b></h3>
                            <p style="font-size:1rem; margin:0.3rem 0 0;">
                                Confidence: <b>{confidence}%</b>
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("No predictions returned.")
            else:
                st.error("❌ Prediction failed or returned empty result.")

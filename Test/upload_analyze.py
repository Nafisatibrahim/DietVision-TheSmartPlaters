"""
Upload & Analyze Page
Users can upload meal photos for AI-based food recognition and nutrition analysis.
Send uploaded image to Vertex AI endpoint and display prediction.
"""

import streamlit as st
import tempfile
import json
from Backend.Classification_model.predictor import predict_image_classification
import pandas as pd
import matplotlib.pyplot as plt

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

                    # Reset Ella’s chat so new meal context is included next time
                    st.session_state.pop("ella_chat", None)


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

                     # --- 🔍 Fetch nutritional data from cached database ---
                    df_nutrients = st.session_state.get("nutrient_database", pd.DataFrame())
                    if not df_nutrients.empty:
                        match = df_nutrients[df_nutrients["Food Class"].str.lower() == food_name.lower()]
                        if not match.empty:
                            food_info = match.iloc[0]

                            st.markdown(f"""
                                <div style="background-color:#f8f9fa;padding:15px;border-radius:10px;margin-top:20px;">
                                    <h3 style="color:#2E7D32;">🥗 Nutritional Information (per {food_info['Portion Size']})</h3>
                                    <ul style="line-height:1.7;">
                                        <li><strong>Calories:</strong> {food_info['Calories']} kcal</li>
                                        <li><strong>Protein:</strong> {food_info['Protein']} g</li>
                                        <li><strong>Fat:</strong> {food_info['Fat']} g</li>
                                        <li><strong>Carbs:</strong> {food_info['Carbs']} g</li>
                                        <li><strong>Fiber:</strong> {food_info['Fiber']} g</li>
                                        <li><strong>Sugar:</strong> {food_info['Sugar']} g</li>
                                        <li><strong>Tags:</strong> {food_info['Tags']}</li>
                                    </ul>
                                </div>
                            """, unsafe_allow_html=True)

                            # Store for Ella to access later
                            st.session_state["last_prediction"]["nutrition"] = food_info.to_dict()

                        else:
                            st.warning("⚠️ No nutritional data found for this food item.")
                    else:
                        st.warning("⚠️ Nutrient database not loaded in session.")

                    # Add bar chat of macros
                    if not match.empty:
                        fig, ax = plt.subplots()
                        ax.bar(["Protein", "Fat", "Carbs"], 
                            [food_info["Protein"], food_info["Fat"], food_info["Carbs"]])
                        ax.set_ylabel("grams (g)")
                        ax.set_title(f"Macronutrient Breakdown for {food_name}")
                        st.pyplot(fig)

                else:
                    st.warning("No predictions returned.")
            else:
                st.error("❌ Prediction failed or returned empty result.")

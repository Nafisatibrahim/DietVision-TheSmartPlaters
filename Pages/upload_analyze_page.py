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

                    st.success(f"✅ Prediction: **{food_name}**")

                    # Save to session_state so that chatbot or dashboard can access
                    st.session_state["last_prediction"] = {
                        "food_name": food_name,
                        "confidence": confidence,
                        "all_labels": labels,
                        "all_scores": scores
                    }

                    # Reset Ella's chat so new meal context is included next time
                    st.session_state.pop("ella_chat", None)

                    # Prediction card with gradient and confidence bar
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #81C784 0%, #4CAF50 100%);
                        border-radius: 15px;
                        padding: 1.5rem;
                        margin: 1.5rem 0;
                        box-shadow: 0 8px 20px rgba(76, 175, 80, 0.3);
                        color: white;
                    ">
                        <h3 style="margin:0; color: white;">🍕 Prediction: <b>{food_name}</b></h3>
                        <div style="display: flex; align-items: center; margin-top: 0.8rem;">
                            <span style="font-size: 1.1rem;">Confidence: <strong>{confidence}%</strong></span>
                            <div style="flex-grow: 1; margin-left: 1rem; background: rgba(255,255,255,0.3); border-radius: 10px; height: 10px;">
                                <div style="width: {confidence}%; background: white; height: 100%; border-radius: 10px; transition: width 0.5s;"></div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # --- 🔍 Fetch nutritional data from cached database ---
                    df_nutrients = st.session_state.get("nutrient_database", pd.DataFrame())
                    if not df_nutrients.empty:
                
                        # Normalize and match more flexibly
                        df_nutrients["Food Class"] = (
                            df_nutrients["Food Class"].str.lower().str.replace("_", " ").str.strip()
                        )
                        food_name_clean = food_name.lower().replace("_", " ").strip()

                        # Try partial and fuzzy matching
                        match = df_nutrients[
                            df_nutrients["Food Class"].str.contains(food_name_clean, na=False)
                        ]

                        # If still no match, try reversed order (e.g., "chicken grilled" -> "grilled chicken")
                        if match.empty:
                            reversed_name = " ".join(reversed(food_name_clean.split()))
                            match = df_nutrients[
                                df_nutrients["Food Class"].str.contains(reversed_name, na=False)
                            ]

                        if not match.empty:
                            food_info = match.iloc[0]

                            # Beautiful Nutritional Information Display
                            st.markdown(f"### 🥗 Nutritional Information (per {food_info['Portion Size']})")
                            
                            # BIG Calorie Card
                            st.markdown(f"""
                            <div style="
                                background: linear-gradient(135deg, #FF6F00 0%, #FF9800 100%);
                                border-radius: 15px;
                                padding: 2rem;
                                margin-bottom: 1.5rem;
                                box-shadow: 0 8px 20px rgba(255, 111, 0, 0.3);
                                text-align: center;
                                color: white;
                            ">
                                <div style="font-size: 1rem; opacity: 0.9; letter-spacing: 2px;">🔥 CALORIES</div>
                                <div style="font-size: 3rem; font-weight: bold; margin: 0.5rem 0;">{food_info['Calories']}</div>
                                <div style="font-size: 1.1rem; opacity: 0.9;">kcal</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Macronutrients Section
                            st.markdown("**💪 Macronutrients**")
                            
                            # Protein Card
                            st.markdown(f"""
                            <div style="
                                background: linear-gradient(135deg, #E91E63 0%, #F06292 100%);
                                border-radius: 12px;
                                padding: 1.2rem;
                                margin-bottom: 0.8rem;
                                box-shadow: 0 4px 12px rgba(233, 30, 99, 0.3);
                                display: flex;
                                justify-content: space-between;
                                align-items: center;
                                color: white;
                            ">
                                <div style="display: flex; align-items: center; gap: 0.7rem;">
                                    <span style="font-size: 1.5rem;">🥩</span>
                                    <span style="font-weight: 500; font-size: 1.1rem;">Protein</span>
                                </div>
                                <div style="font-size: 1.8rem; font-weight: bold;">{food_info['Protein']}g</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Fat Card
                            st.markdown(f"""
                            <div style="
                                background: linear-gradient(135deg, #9C27B0 0%, #BA68C8 100%);
                                border-radius: 12px;
                                padding: 1.2rem;
                                margin-bottom: 0.8rem;
                                box-shadow: 0 4px 12px rgba(156, 39, 176, 0.3);
                                display: flex;
                                justify-content: space-between;
                                align-items: center;
                                color: white;
                            ">
                                <div style="display: flex; align-items: center; gap: 0.7rem;">
                                    <span style="font-size: 1.5rem;">🧈</span>
                                    <span style="font-weight: 500; font-size: 1.1rem;">Fat</span>
                                </div>
                                <div style="font-size: 1.8rem; font-weight: bold;">{food_info['Fat']}g</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Carbs Card
                            st.markdown(f"""
                            <div style="
                                background: linear-gradient(135deg, #FFC107 0%, #FFD54F 100%);
                                border-radius: 12px;
                                padding: 1.2rem;
                                margin-bottom: 1.5rem;
                                box-shadow: 0 4px 12px rgba(255, 193, 7, 0.3);
                                display: flex;
                                justify-content: space-between;
                                align-items: center;
                                color: white;
                            ">
                                <div style="display: flex; align-items: center; gap: 0.7rem;">
                                    <span style="font-size: 1.5rem;">🍞</span>
                                    <span style="font-weight: 500; font-size: 1.1rem;">Carbs</span>
                                </div>
                                <div style="font-size: 1.8rem; font-weight: bold;">{food_info['Carbs']}g</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Micronutrients Section
                            st.markdown("**🌱 Micronutrients**")
                            
                            col_micro1, col_micro2 = st.columns(2)
                            
                            with col_micro1:
                                # Fiber Card
                                st.markdown(f"""
                                <div style="
                                    background: linear-gradient(135deg, #8BC34A 0%, #AED581 100%);
                                    border-radius: 10px;
                                    padding: 1rem;
                                    box-shadow: 0 3px 10px rgba(139, 195, 74, 0.3);
                                    text-align: center;
                                    color: white;
                                ">
                                    <div style="font-size: 1.1rem;">🌾 Fiber</div>
                                    <div style="font-size: 1.5rem; font-weight: bold; margin-top: 0.3rem;">{food_info['Fiber']}g</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with col_micro2:
                                # Sugar Card
                                st.markdown(f"""
                                <div style="
                                    background: linear-gradient(135deg, #FF5722 0%, #FF7043 100%);
                                    border-radius: 10px;
                                    padding: 1rem;
                                    box-shadow: 0 3px 10px rgba(255, 87, 34, 0.3);
                                    text-align: center;
                                    color: white;
                                ">
                                    <div style="font-size: 1.1rem;">🍯 Sugar</div>
                                    <div style="font-size: 1.5rem; font-weight: bold; margin-top: 0.3rem;">{food_info['Sugar']}g</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            # Tags
                            if food_info.get('Tags'):
                                st.markdown(f"""
                                <div style="
                                    background: rgba(129, 199, 132, 0.1);
                                    border: 2px solid #81C784;
                                    border-radius: 10px;
                                    padding: 1rem;
                                    margin-top: 1.5rem;
                                ">
                                    <div style="color: #2E7D32; font-weight: 600; margin-bottom: 0.5rem;">🏷️ Tags:</div>
                                    <div style="color: #555;">{food_info['Tags']}</div>
                                </div>
                                """, unsafe_allow_html=True)

                            # Store for Ella to access later
                            st.session_state["last_prediction"]["nutrition"] = food_info.to_dict()

                            # Bar chart of macros (improved styling)
                            st.markdown("### 📊 Macronutrient Breakdown")
                            fig, ax = plt.subplots(figsize=(8, 4))
                            colors = ['#E91E63', '#9C27B0', '#FFC107']
                            bars = ax.bar(["Protein", "Fat", "Carbs"], 
                                [food_info["Protein"], food_info["Fat"], food_info["Carbs"]],
                                color=colors)
                            ax.set_ylabel("Grams (g)", fontsize=11)
                            ax.set_title(f"Macronutrient Breakdown for {food_name}", fontsize=13, fontweight='bold')
                            ax.grid(axis='y', alpha=0.3)
                            plt.tight_layout()
                            st.pyplot(fig)

                        else:
                            st.warning("⚠️ No nutritional data found for this food item.")
                    else:
                        st.warning("⚠️ Nutrient database not loaded in session.")

                else:
                    st.warning("No predictions returned.")
            else:
                st.error("❌ Prediction failed or returned empty result.")

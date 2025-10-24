"""
Dashboard Page
Displays nutritional statistics and recent meal history.
"""

import streamlit as st
import pandas as pd

def show(user):
    """Render the dashboard with nutrition metrics and trends."""
    st.title("📊 Your Nutrition Dashboard")

    # Check if there’s any logged data
    if len(st.session_state.meal_history) == 0:
        st.info("📝 No meals logged yet. Upload a food image to get started!")

        # --- Optional mock data for preview ---
        st.markdown("### 📊 Sample Dashboard Preview")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🔥 Daily Calories", "1,847", "↗️ 125")
        with col2:
            st.metric("🥩 Protein", "78g", "↗️ 12g")
        with col3:
            st.metric("🍽️ Meals Today", "3", "→ 0")
        with col4:
            st.metric("💧 Water Intake", "6 cups", "↗️ 2")

        sample_data = pd.DataFrame({
            "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "Calories": [1650, 1820, 1740, 1950, 1680, 2100, 1890]
        })
        st.line_chart(sample_data.set_index("Day"))
        return

    # --- Actual dashboard content ---
    df = pd.DataFrame(st.session_state.meal_history)

    st.markdown(f"### 👤 Hello, {user.get('name')}! Here’s your nutrition overview:")

    # 🔹 Nutrition Summary Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_calories = df["calories"].sum()
        st.metric("🔥 Total Calories", f"{total_calories:,}")
    with col2:
        avg_protein = df["protein"].mean()
        st.metric("🥩 Avg Protein", f"{avg_protein:.1f}g")
    with col3:
        total_meals = len(df)
        st.metric("🍽️ Meals Logged", total_meals)
    with col4:
        avg_calories = df["calories"].mean()
        st.metric("📊 Avg Calories/Meal", f"{avg_calories:.0f}")

    st.markdown("---")

    # 🔹 Macronutrient Breakdown
    st.markdown("### 🥗 Macronutrient Breakdown")

    macros_df = pd.DataFrame({
        "Nutrient": ["Protein", "Carbs", "Fat"],
        "Grams": [
            df["protein"].sum(),
            df["carbs"].sum(),
            df["fat"].sum(),
        ],
    })

    st.bar_chart(macros_df.set_index("Nutrient"))

    # 🔹 Calories Over Time
    if "timestamp" in df.columns:
        st.markdown("### 📈 Calories Over Time")
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        chart_df = df[["timestamp", "calories"]].set_index("timestamp")
        st.line_chart(chart_df)

    # 🔹 Recent Meals
    st.markdown("### 🧾 Recent Meals")
    display_df = df[["food_name", "calories", "protein", "carbs", "fat", "timestamp"]].copy()
    display_df["timestamp"] = pd.to_datetime(display_df["timestamp"]).dt.strftime("%Y-%m-%d %H:%M")
    st.dataframe(display_df, use_container_width=True)



# Later: add filters
"""
period = st.selectbox("📅 Select Period", ["Daily", "Weekly", "Monthly"])
"""
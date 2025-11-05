"""
Dashboard Page
Displays nutritional statistics, meal history, and recent meal history.
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random

def show_dashboard_page(user):
    """Dashboard with meal history and statistics"""
    
    # Check if user is signed in
    if not user or not isinstance(user, dict):
        st.warning("⚠️ Please sign in to view your dashboard.")
        return
    
    st.title("📊 Your Nutrition Dashboard")

    # Prototype notice banner
    st.markdown("""
    <div style="
        background-color: #FFF3E0;
        border-left: 6px solid #FF9800;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1.5rem;
    ">
        <strong>⚠️ Prototype Notice:</strong>  
        This dashboard is a <strong>sample visualization</strong> created for the prototype of <em>DietVision.ai</em>.  
        It currently displays sample data for demonstration purposes.  
        Future versions will include real-time updates from your uploaded meals and personalized analytics.
    </div>
    """, unsafe_allow_html=True)

    
    # Welcome message with gradient
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #81C784 0%, #FF9800 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 20px rgba(76, 175, 80, 0.3);
        color: white;
        text-align: center;
    ">
        <h2 style="margin:0; color: white;">👋 Welcome back, {user.get("name", "User").split()[0]}!</h2>
        <p style="margin:0.5rem 0 0 0; font-size: 1.1rem;">Track your nutrition journey and achieve your goals 🎯</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Time period selector
    col_period, col_filter = st.columns([2, 3])
    with col_period:
        period = st.selectbox("📅 Time Period", 
                             ["Today", "This Week", "This Month", "All Time"],
                             help="Choose the time period for your nutrition statistics")
    
    with col_filter:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        st.caption(f"📌 Showing data for: **{period}**")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Check if there's meal history
    meal_history = st.session_state.get("meal_history", [])
    
    if len(meal_history) > 0:
        # Convert to DataFrame
        df = pd.DataFrame(meal_history)
        
        # Filter by time period (mock filtering for now)
        if period == "Today":
            display_period = "Today"
        elif period == "This Week":
            display_period = "This Week"
        elif period == "This Month":
            display_period = "This Month"
        else:
            display_period = "All Time"
        
        # === SUMMARY METRICS ===
        st.markdown("### 📈 Nutrition Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_calories = df['calories'].sum()
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #FF6F00 0%, #FF9800 100%);
                border-radius: 12px;
                padding: 1.2rem;
                text-align: center;
                color: white;
                box-shadow: 0 4px 15px rgba(255, 111, 0, 0.3);
            ">
                <div style="font-size: 0.9rem; opacity: 0.9;">🔥 Total Calories</div>
                <div style="font-size: 2rem; font-weight: bold; margin: 0.3rem 0;">{total_calories:,}</div>
                <div style="font-size: 0.8rem; opacity: 0.8;">kcal</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_protein = df['protein'].mean()
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #E91E63 0%, #F06292 100%);
                border-radius: 12px;
                padding: 1.2rem;
                text-align: center;
                color: white;
                box-shadow: 0 4px 15px rgba(233, 30, 99, 0.3);
            ">
                <div style="font-size: 0.9rem; opacity: 0.9;">🥩 Avg Protein</div>
                <div style="font-size: 2rem; font-weight: bold; margin: 0.3rem 0;">{avg_protein:.1f}</div>
                <div style="font-size: 0.8rem; opacity: 0.8;">grams/meal</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_meals = len(df)
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
                border-radius: 12px;
                padding: 1.2rem;
                text-align: center;
                color: white;
                box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
            ">
                <div style="font-size: 0.9rem; opacity: 0.9;">🍽️ Meals Logged</div>
                <div style="font-size: 2rem; font-weight: bold; margin: 0.3rem 0;">{total_meals}</div>
                <div style="font-size: 0.8rem; opacity: 0.8;">meals</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            avg_calories = df['calories'].mean()
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #9C27B0 0%, #BA68C8 100%);
                border-radius: 12px;
                padding: 1.2rem;
                text-align: center;
                color: white;
                box-shadow: 0 4px 15px rgba(156, 39, 176, 0.3);
            ">
                <div style="font-size: 0.9rem; opacity: 0.9;">📊 Avg Calories</div>
                <div style="font-size: 2rem; font-weight: bold; margin: 0.3rem 0;">{avg_calories:.0f}</div>
                <div style="font-size: 0.8rem; opacity: 0.8;">kcal/meal</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # === CHARTS SECTION ===
        st.markdown("### 📊 Nutrition Breakdown")
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("**🍴 Macronutrient Distribution**")
            
            # Pie chart for macros
            fig, ax = plt.subplots(figsize=(6, 6))
            macros = [df['protein'].sum(), df['carbs'].sum(), df['fat'].sum()]
            labels = ['Protein', 'Carbs', 'Fat']
            colors = ['#E91E63', '#FFC107', '#9C27B0']
            explode = (0.05, 0.05, 0.05)
            
            ax.pie(macros, labels=labels, colors=colors, autopct='%1.1f%%',
                   startangle=90, explode=explode, shadow=True,
                   textprops={'fontsize': 11, 'weight': 'bold'})
            ax.set_title('Total Macronutrient Distribution', fontsize=13, fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig)
        
        with col_chart2:
            st.markdown("**📈 Calories Over Time**")
            
            # Line chart for calories trend
            fig, ax = plt.subplots(figsize=(6, 6))
            
            # Create x-axis (meal numbers)
            meal_numbers = list(range(1, len(df) + 1))
            calories = df['calories'].tolist()
            
            ax.plot(meal_numbers, calories, marker='o', color='#FF6F00', 
                   linewidth=2, markersize=8, markerfacecolor='#FF9800', 
                   markeredgecolor='white', markeredgewidth=2)
            ax.fill_between(meal_numbers, calories, alpha=0.3, color='#FFF3E0')
            ax.set_xlabel('Meal Number', fontsize=11, fontweight='bold')
            ax.set_ylabel('Calories (kcal)', fontsize=11, fontweight='bold')
            ax.set_title('Calorie Intake Trend', fontsize=13, fontweight='bold')
            ax.grid(True, alpha=0.3, linestyle='--')
            plt.tight_layout()
            st.pyplot(fig)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # === MICRONUTRIENTS BAR CHART ===
        st.markdown("### 🌾 Micronutrient Summary")
        
        fig, ax = plt.subplots(figsize=(10, 4))
        nutrients = ['Fiber', 'Sugar']
        values = [df['fiber'].sum(), df['sugar'].sum()]
        colors_micro = ['#4CAF50', '#FF5722']
        
        bars = ax.bar(nutrients, values, color=colors_micro, alpha=0.8, edgecolor='white', linewidth=2)
        ax.set_ylabel('Grams (g)', fontsize=11, fontweight='bold')
        ax.set_title('Total Fiber and Sugar Intake', fontsize=13, fontweight='bold')
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}g', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # === MEAL HISTORY TABLE ===
        st.markdown("### 📝 Recent Meals")
        
        # Create display dataframe
        display_df = df[['food_name', 'calories', 'protein', 'carbs', 'fat', 'fiber', 'sugar', 'timestamp']].copy()
        display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        display_df.columns = ['Food', 'Calories', 'Protein (g)', 'Carbs (g)', 'Fat (g)', 'Fiber (g)', 'Sugar (g)', 'Time']
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Food": st.column_config.TextColumn("🍕 Food", width="medium"),
                "Calories": st.column_config.NumberColumn("🔥 Calories", format="%d kcal"),
                "Protein (g)": st.column_config.NumberColumn("🥩 Protein", format="%d g"),
                "Carbs (g)": st.column_config.NumberColumn("🍞 Carbs", format="%d g"),
                "Fat (g)": st.column_config.NumberColumn("🧈 Fat", format="%d g"),
                "Fiber (g)": st.column_config.NumberColumn("🌾 Fiber", format="%d g"),
                "Sugar (g)": st.column_config.NumberColumn("🍯 Sugar", format="%d g"),
                "Time": st.column_config.TextColumn("🕐 Time", width="small"),
            }
        )
        
    else:
        # === EMPTY STATE WITH SAMPLE DATA ===
        st.info("📝 No meals logged yet. Upload some food images to get started!")
        
        st.markdown("### 📊 Sample Dashboard Preview")
        st.caption("This is how your dashboard will look once you start logging meals!")
        
        # Mock metrics with gradient cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #FF6F00 0%, #FF9800 100%);
                border-radius: 12px;
                padding: 1.2rem;
                text-align: center;
                color: white;
                box-shadow: 0 4px 15px rgba(255, 111, 0, 0.3);
            ">
                <div style="font-size: 0.9rem; opacity: 0.9;">🔥 Daily Calories</div>
                <div style="font-size: 2rem; font-weight: bold; margin: 0.3rem 0;">1,847</div>
                <div style="font-size: 0.8rem; opacity: 0.8; color: #90EE90;">↗️ +125</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #E91E63 0%, #F06292 100%);
                border-radius: 12px;
                padding: 1.2rem;
                text-align: center;
                color: white;
                box-shadow: 0 4px 15px rgba(233, 30, 99, 0.3);
            ">
                <div style="font-size: 0.9rem; opacity: 0.9;">🥩 Protein</div>
                <div style="font-size: 2rem; font-weight: bold; margin: 0.3rem 0;">78g</div>
                <div style="font-size: 0.8rem; opacity: 0.8; color: #90EE90;">↗️ +12g</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
                border-radius: 12px;
                padding: 1.2rem;
                text-align: center;
                color: white;
                box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
            ">
                <div style="font-size: 0.9rem; opacity: 0.9;">🍽️ Meals Today</div>
                <div style="font-size: 2rem; font-weight: bold; margin: 0.3rem 0;">3</div>
                <div style="font-size: 0.8rem; opacity: 0.8;">→ on track</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #2196F3 0%, #64B5F6 100%);
                border-radius: 12px;
                padding: 1.2rem;
                text-align: center;
                color: white;
                box-shadow: 0 4px 15px rgba(33, 150, 243, 0.3);
            ">
                <div style="font-size: 0.9rem; opacity: 0.9;">💧 Water Intake</div>
                <div style="font-size: 2rem; font-weight: bold; margin: 0.3rem 0;">6</div>
                <div style="font-size: 0.8rem; opacity: 0.8;">cups today</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Sample chart
        st.markdown("### 📈 Weekly Calorie Trend (Sample)")
        
        sample_data = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Calories': [1650, 1820, 1740, 1950, 1680, 2100, 1890]
        })
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(sample_data['Day'], sample_data['Calories'], 
               marker='o', color='#FF6F00', linewidth=3, markersize=10,
               markerfacecolor='#FF9800', markeredgecolor='white', markeredgewidth=2)
        ax.fill_between(range(len(sample_data)), sample_data['Calories'], 
                        alpha=0.3, color='#FFF3E0')
        ax.set_xlabel('Day of Week', fontsize=12, fontweight='bold')
        ax.set_ylabel('Calories (kcal)', fontsize=12, fontweight='bold')
        ax.set_title('Sample Weekly Calorie Intake', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.axhline(y=2000, color='red', linestyle='--', alpha=0.5, label='Target: 2000 kcal')
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Call to action
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #E8F5E8, #FFF3E0);
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            border: 2px solid #81C784;
        ">
            <h3 style="color: #2E7D32; margin: 0;">🚀 Ready to start tracking?</h3>
            <p style="color: #555; margin: 0.5rem 0 0 0;">
                Head over to <strong>Upload & Analyze</strong> to log your first meal!
            </p>
        </div>
        """, unsafe_allow_html=True)
    st.caption("⚙️ Note: This dashboard currently uses sample data. Actual meal logging and live statistics are part of future development.")

if __name__ == "__main__":
    show_dashboard_page(st.user)
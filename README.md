# 🍽️ DietVision.ai — Your AI-Powered Nutrition Assistant
## Women in AI Canada Hackathon 2025

**DietVision.ai** is a Streamlit-based prototype that uses AI and computer vision to analyze meals, provide nutritional insights, and offer personalized diet recommendations through an intelligent chatbot named **Ella**.

This project was developed as part of the **Women in AI Hackathon 2025** to demonstrate how AI can make nutrition **accessible, personalized, and data-driven**.

---

## 🌟 Features

✅ **Image-based food recognition**
- Upload a meal photo, and the app predicts what it is using a Vertex AI image classification model.  
- Displays calorie count and full nutritional breakdown.

💬 **Chat with Ella**
- Ella provides nutrition tips and tailored recommendations based on your health profile.
- Profile-aware: for example, users with high cholesterol receive low-fat food advice.

👤 **User Profiles**
- Sign in securely via Google OAuth2.
- Save personal details, preferences, health goals, and dietary restrictions.

📊 **Nutrition Dashboard**
- Visualize macronutrients, calories, and sample trends.
- Note: currently a prototype — live tracking and meal logging will be added in future updates.

💚 **Feedback Page**
- Users can rate their experience and submit feedback directly from the app.
- All responses are saved securely to Google Sheets via the service account.

---

## 🏗️ Tech Stack

| Component | Technology |
|------------|-------------|
| Frontend | Streamlit |
| Backend | Python (FastAPI-like structure within Streamlit) |
| Authentication | Google OAuth2 |
| AI Model | Vertex AI AutoML Image Classification |
| Storage | Google Sheets + CSV fallback |
| Visualization | Matplotlib, Pandas |
| Deployment | Streamlit Cloud |
| Database | CSV (prototype), Google Sheets (cloud sync) |

---

## 🔐 Authentication & Data Privacy

- OAuth2 authentication is handled securely via Google Sign-In.
- User data (profiles, preferences, feedback) is stored in **Google Sheets** under your service account.
- No data is shared publicly; this project is for demonstration and educational purposes only.

---

## 🚀 How to Run Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/NafisatIbrahim/DietVision-TheSmartPlaters.git
cd DietVision-TheSmartPlaters


<div class="chat-button" onclick="window.parent.postMessage('toggle_chat', '*')">
    <img src="https://cdn-icons-png.flaticon.com/512/4712/4712027.png" width="32"/>
</div>
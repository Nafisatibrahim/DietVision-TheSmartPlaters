import os
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GRPC_CPP_MIN_LOG_LEVEL"] = "3"

import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define generation controls
generation_config = {
    "max_output_tokens": 512,
    "temperature": 0.6,
    "top_p": 0.8,
    "top_k": 40
}

# Define the model to be used
model = genai.GenerativeModel(
    model_name = "gemini-2.5-flash",
    generation_config=generation_config
    )

def generate_response(prompt):
    #Generate a response from the Gemini model based on the given prompt.
    try:
        system_prompt = (
            "You are DietVision.ai, a friendly and concise AI nutrition assistant. "
            "Reply in under 3 sentences unless the user explicitly asks for a longer explanation. "
            "Avoid lists or bullet points unless requested. "
            "Be warm, conversational, and direct."
        )
        # Combine style + user message into one prompt
        full_prompt = f"{system_prompt}\nUser: {prompt}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error generating response: {e}"
    
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        print("Gemini:", generate_response(user_input))

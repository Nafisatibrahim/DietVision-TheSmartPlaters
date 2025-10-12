import streamlit as st

# Page setup
st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="wide")

# Title
st.title("🤖 Chatbot Application")

# Text
st.write("This is just a quick demo to see if a Chatbot is feasible in Streamlit.")

# Input box
name = st.text_input("Enter your name:", "")
if name:
    st.write(f"Hello, {name}! Welcome to the Chatbot application.")
else:
    st.write("Please enter your name to get started.")

age = st.number_input("Enter your age:", min_value=0, max_value=120, value=25)
st.write(f"You are {age} years old.")
if age < 18:
    st.write("You are a minor.")
elif age < 65:
    st.write("You are an adult.")
else:
    st.write("You are a senior citizen.")
# Button
if st.button("Submit"):
    st.write("Thank you for submitting your information!")



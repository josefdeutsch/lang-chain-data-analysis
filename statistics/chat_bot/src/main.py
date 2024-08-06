import os
import requests
import streamlit as st

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

CHAT_API = os.getenv("CHAT_API")
ANALYTICS = os.getenv("ANALYTICS")

st.title("Hospital System Chatbot")
st.info("Ask me questions about patients, visits, insurance payers, hospitals, physicians, reviews, and wait times!")

# Message to send
message_to_send = {"message": "A message from the chatbot!"}

# Send POST request
response = requests.post(CHAT_API, json=message_to_send)

if response.status_code == 200:
    st.write(response.json())
else:
    st.write(response.status_code)




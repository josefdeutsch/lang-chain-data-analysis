import os
import requests
import streamlit as st

CHATBOT_URL = os.getenv("CHATBOT_URL", "http://chat_api:8000/chat")

st.title("Hospital System Chatbot")
st.info("Ask me questions about patients, visits, insurance payers, hospitals, physicians, reviews, and wait times!")

# Message to send
message_to_send = {"message": "A message from the chatbot!"}

# Send POST request
response = requests.post(CHATBOT_URL, json=message_to_send)

if response.status_code == 200:
    st.write(response.json())
else:
    st.write(response.status_code)




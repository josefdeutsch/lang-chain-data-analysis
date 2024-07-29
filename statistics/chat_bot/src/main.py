import os
import requests
import streamlit as st

CHATBOT_URL = os.getenv("CHATBOT_URL", "http://chat_api:8000/helloworld")

st.title("Hospital System Chatbot")
st.info("Ask me questions about patients, visits, insurance payers, hospitals, physicians, reviews, and wait times!")

response = requests.get(CHATBOT_URL)

if response.status_code == 200:
    st.write(response.json())
else:
    st.write("Error: Unable to get response from the chatbot")

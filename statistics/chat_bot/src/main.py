import os
import requests
import streamlit as st

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

CHAT_API = os.getenv("CHAT_API")


with st.sidebar:
    st.header("About")
    st.markdown(
        """
        This chatbot is equipped with a [LangChain](https://python.langchain.com/docs/get_started/introduction) 
        agent tailored to answer questions about the stock market, specifically focusing on Bitcoin and Ethereum data 
        from the last four years (from August 8, 2020, to the present, with ongoing updates). 
        The agent utilizes retrieval-augmented generation (RAG) techniques to deliver insights, 
        pulling from both structured and unstructured datasets that have been synthetically generated.
        """
    )

   


st.title("Stock Market Chatbot")
st.info(
    """Feel free to ask me questions about Ethereum and Bitcoin data, including information on
      Date, Open, High, Low, Close, Adjusted Close, and Volume, up until August 8, 2020."""
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message.keys():
            st.markdown(message["output"])

        if "explanation" in message.keys():
            with st.status("How was this generated", state="complete"):
                st.info(message["explanation"])

if prompt := st.chat_input("What do you want to know?"):
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user", "output": prompt})

    data = {"text": prompt}

    with st.spinner("Searching for an answer..."):
        response = requests.post(CHAT_API, json=data)

        if response.status_code == 200:
            output_text = response.json()["output"]
            explanation = response.json()["intermediate_steps"]

        else:
            output_text = """An error occurred while processing your message.
            Please try again or rephrase your message."""
            explanation = output_text

    st.chat_message("assistant").markdown(output_text)
    st.status("How was this generated?", state="complete").info(explanation)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": output_text,
            "explanation": explanation,
        }
    )




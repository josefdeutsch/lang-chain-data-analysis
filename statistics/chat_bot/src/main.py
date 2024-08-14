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

    st.header("Example Questions")

    st.markdown("- What is the lowest recorded price for BTCUSD?")
    st.markdown("- What is the highest recorded price for BTCUSD?")
    st.markdown("- What is the average closing price of BTCUSD?")
    st.markdown("- What is the total volume of BTCUSD traded?")
    st.markdown("- What is the difference between the highest and lowest prices for each day from July 1, 2024, to August 1, 2024?")
    st.markdown("- What is the percentage change between the opening and closing prices for each day from July 1, 2024, to August 1, 2024?")
    st.markdown("- What is the median closing price of BTCUSD?")
    st.markdown("- What is the range between the highest and lowest prices ever recorded for BTCUSD?")
    st.markdown("- On which date was the trading volume for BTCUSD the highest?")
    st.markdown("- What is the standard deviation of BTCUSD closing prices?")
    st.markdown("- How many trading days are recorded in the dataset?")
    st.markdown("- What is the cumulative return percentage from August 8, 2020, to August 15, 2020, for BTCUSD?")
    st.markdown("- What is the average daily trading range (difference between the highest and lowest prices) for BTCUSD?")
    st.markdown("- Which days between August 8, 2020, and August 15, 2020, had a closing price higher than the opening price for BTCUSD?")
    st.markdown("- What is the 7-day rolling average of closing prices for BTCUSD from August 1st 2024 to August 7th 2024?")
    st.markdown("- What is the highest adjusted closing price for BTCUSD between August 8, 2020, and August 15, 2020?")
    st.markdown("- How many days had a trading volume greater than 25,000,000,000 for BTCUSD?")

    


    st.markdown("- What is the lowest recorded price for BTCUSD?")
    st.markdown("- What is the highest recorded price for BTCUSD?")
    st.markdown("- What is the average closing price of BTCUSD?")
    st.markdown("- What is the total volume of BTCUSD traded?")
    st.markdown("- What is the range between the highest and lowest prices ever recorded for BTCUSD?")
    st.markdown("- What is the 7-day rolling average of closing prices for BTCUSD from August 1st 2024 to August 7th 2024?")
    st.markdown("- What is the standard deviation of BTCUSD closing prices?")
    st.markdown("- On which date was the trading volume for BTCUSD the highest?")
    st.markdown("- Did Bitcoin's closing prices remain consistent without showing any clear trend between July 1, 2024, and August 1, 2024?")
    st.markdown("- Are the closing prices of Bitcoin and Ethereum related, and do they move together over time between July 1, 2024, and August 1, 2024?")

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




import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

CHAT_API = os.getenv("CHAT_API")
ANALYTICS = os.getenv("ANALYTICS")

app = FastAPI(
    title="Simple Chatbot",
    description="A simple chatbot server with a POST endpoint",
)

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/")
async def get_status():
    return {"status": "running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):

    # Message to send
    message_to_send = {"message": ""}

    # Send POST request
    response = requests.post(ANALYTICS, json=message_to_send)

    if response.status_code == 200:
        processed_message = f"Received your message: '{message.message}'. This is a response from the chatbot. '{response.json()}"
    
    
    # Return the processed message
    return {"response": processed_message}


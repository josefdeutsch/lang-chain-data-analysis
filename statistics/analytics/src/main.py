import os
from fastapi import FastAPI
from pydantic import BaseModel
from timeseries.cointegration import calculate_optimal_hedge_ratio_and_cadf


CHAT_API = os.getenv("CHAT_API", "http://chat_api:8031/chat")
ANALYTICS = os.getenv("ANALYTICS", "http://analytics:8032/adf")

app = FastAPI(
    title="Simple Chatbot",
    description="A simple chatbot server with a POST endpoint",
)

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/adf", response_model=ChatResponse)
async def adf(message: ChatMessage):
    processed_message = f"Received your message: '{message.message}'"
    
    # Return the processed message
    return processed_message
    
@app.post("/hello", response_model=ChatResponse)
async def hello(message: ChatMessage):
    processed_message = f"Received your message: '{message.message}'"
    # Simulate a call to the analytics service
    return ChatResponse(response=processed_message)




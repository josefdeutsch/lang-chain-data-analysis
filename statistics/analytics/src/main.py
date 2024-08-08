import json
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
    # Convert JSON string back to dictionary
    data = json.loads(message.message)

    # Accessing the data
    ts1 = data["ts1"]
    ts2 = data["ts2"]

    adf_results = calculate_optimal_hedge_ratio_and_cadf(ts1, ts2)
    
    processed_message = (
        f"Received your message: '{message.message}'.\n"
        f"Optimal Hedge Ratio (Beta): {adf_results['beta_hr']}\n"
        "CADF Test Results:\n"
        f"ADF Statistic: {adf_results['cadf'][0]}\n"
        f"p-value: {adf_results['cadf'][1]}\n"
        "Critical Values:\n"
    )
    for key, value in adf_results['cadf'][4].items():
        processed_message += f"\t{key}: {value}\n"
    
    processed_message += f"Lengths of time series: {len(ts1)}, {len(ts2)}"
    
    # Return the processed message
    return ChatResponse(response=processed_message)
    
@app.post("/hello", response_model=ChatResponse)
async def hello(message: ChatMessage):
    processed_message = f"Received your message: '{message.message}'"
    # Simulate a call to the analytics service
    return ChatResponse(response=processed_message)




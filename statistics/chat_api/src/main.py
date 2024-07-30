from fastapi import FastAPI
from pydantic import BaseModel

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
    # Simulate processing the message (e.g., appending a response)
    processed_message = f"Received your message: '{message.message}'. This is a response from the chatbot."
    
    # Return the processed message
    return {"response": processed_message}



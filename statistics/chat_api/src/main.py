from agents.chat_api_agent import chat_api_agent_executor
from fastapi import FastAPI
from models.chat_api_query import ChatApiQueryInput, ChatApiOutput
from utils.async_utils import async_retry
from dotenv import load_dotenv
load_dotenv()
app = FastAPI(
    title="Chat_Api",
    description="Endpoints for a chat_api system RAG chatbot",
)


@async_retry(max_retries=20, delay=1)
async def invoke_agent_with_retry(query: str):
    """
    Retry the agent if a tool fails to run. This can help when there
    are intermittent connection issues to external APIs.
    """

    return await chat_api_agent_executor.ainvoke({"input": query})


@app.get("/")
async def get_status():
    return {"status": "running"}


@app.post("/chat")
async def query_chat_api_agent(
    query: ChatApiQueryInput,
) -> ChatApiOutput:
    query_response = await invoke_agent_with_retry(query.text)
    query_response["intermediate_steps"] = [
        str(s) for s in query_response["intermediate_steps"]
    ]

    return query_response




import os
import threading
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_tools_agent, Tool
from langchain import hub
from langchain_openai import ChatOpenAI
from tools.wrapper import stock_cypher_chain_exec


load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv('LANGCHAIN_TRACING_V2')
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')

CHAT_API_MODEL = os.getenv("CHAT_API_MODEL")

chat_api_prompt = hub.pull("hwchase17/openai-functions-agent")

tools = [
    stock_cypher_chain_exec
]  

chat_model = ChatOpenAI(
    model=CHAT_API_MODEL,
    temperature=0,
)

chat_api_agent = create_openai_tools_agent(
    llm=chat_model,
    prompt=chat_api_prompt,
    tools=tools,
)


chat_api_agent_executor = AgentExecutor(
    agent=chat_api_agent,
    tools=tools,
    return_intermediate_steps=True,
    verbose=True,
)



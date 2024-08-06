import os
import threading
from dotenv import load_dotenv
from tools.cointegration import example_tool
from langchain.agents import AgentExecutor, create_openai_tools_agent, Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI


load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv('LANGCHAIN_TRACING_V2')
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')

CHAT_API_MODEL = os.getenv("CHAT_API_MODEL")

chat_api_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "An exceptionally accurate and precise agent processes all input data and delivers comprehensive results, ensuring no information is omitted. This dependable assistant efficiently uses available tools to answer questions, returning all relevant data, and promptly notifying you if any tool is unavailable."),
                ("user", "{input}"),
                MessagesPlaceholder("chat_history", optional=True),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

tools = [
    Tool(
        name="Example",
        func=example_tool,
        description="""This function is designed to take a single string input and return a personalized 
        greeting message. Specifically, it transforms an input string such as "hello" into "hello from example tool." 
        This function is particularly useful for creating friendly, automated responses based on simple input strings. 
        It is ideal for demonstrating basic string manipulation in programming tutorials and for scenarios where a quick 
        and straightforward transformation of input to a friendly output is required. However, it should not be used for 
        complex string operations, non-string inputs, or advanced text processing tasks. For instance, given the 
        input "hello," the function will return "hello from example tool.""",
    ),
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



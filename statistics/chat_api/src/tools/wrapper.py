import os
from typing import Any
from chains.stock_cypher_chain import stock_cypher_chain
# Import things that are needed generically
from langchain.tools import tool

def example_tool(input_string):
    """
    This function takes a string input and returns a personalized greeting message.

    Args:
    input_string (str): The input string to be transformed into a greeting.

    Returns:
    str: A personalized greeting message.
    """
    return f"{input_string} from example tool"

@tool
def stock_cypher_chain_exec(query: str) -> Any:
    """
    Useful for answering questions about stock prices, trading volumes,
    and daily stock statistics. Use the entire prompt as input to the tool.
    For instance, if the prompt is "What was the highest closing price?",
    the input should be "What was the highest closing price?".
    
    Args:
        query (str): The query string related to stock information.
    
    Returns:
        Any: The response from the stock_cypher_chain.
    """
    return stock_cypher_chain.invoke(query)

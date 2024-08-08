import os
from typing import Any
import requests
import json
from chains.stock_cypher_chain import stock_cypher_chain
from tools.math.stat import calculate_optimal_hedge_ratio_and_cadfs,calculate_hurst_exponents
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()
ANALYTICS = os.getenv("ANALYTICS")
HELLO = os.getenv("HELLO")

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
def cyper_stock_chain(query: str) -> Any:
    """
    Useful for answering questions about stock prices, trading volumes,
    and daily stock statistics. Use the entire prompt as input to the tool.
    For instance, if the prompt is "What was the highest closing price?",
    the input should be "What was the highest closing price?".
    
    Args:
        query (str): The query string related to stock information.
    
    Returns:
        Any: The response from the cyper_stock_chain.
    """
    return stock_cypher_chain.invoke(query)


@tool
def calculate_optimal_hedge_ratio_and_cadf(ts1: list, ts2: list) -> Any: 
    """
    Useful for answering questions about optimal hedge ratios, residual analysis, and cointegration tests. 
    Use the entire prompt as input to the tool. For instance, if the prompt is "What is the optimal hedge ratio?", 
    the input should be "What is the optimal hedge ratio?". 

    Parameters:
        ts1 (list): List containing the first time series data.
        ts2 (list): List containing the second time series data.

    Returns:
        dict: A dictionary containing:
            - 'beta_hr' (float): The optimal hedge ratio.
            - 'cadf' (tuple): The results of the CADF test on the residuals.
    """

    # Send the POST request with the original data dictionary
    return calculate_optimal_hedge_ratio_and_cadfs(ts1,ts2)

@tool
def calculate_hurst_exponent(ts1: list) -> Any:
    """
    Useful for answering questions about optimal hedge ratios, residual analysis, 
    and cointegration tests, the Hurst exponent provides critical insights into 
    the behavior of time series data. To utilize this metric, consider the function 
    calculate_hurst_exponent(ts), which computes the Hurst exponent for a given time series. 
    This function is particularly beneficial for understanding long-term dependencies and 
    mean reversion in financial data.
   
    If you need to determine the persistence or mean-reverting nature of a time series, 
    simply input your data series as a list into the tool. For example, if the prompt is 
    "Calculate the Hurst exponent for my time series data," the input should be 
    "Calculate the Hurst exponent for my time series data."

    Parameters:
        ts (list): A list representing the time series data.

    Returns:
        float: The Hurst exponent of the time series. Returns NaN if the time series is 
               too short or if the computation fails.
    """
    return calculate_hurst_exponents(ts1)
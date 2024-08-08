from statsmodels.api import OLS
from statsmodels.tsa.stattools import adfuller
import numpy as np

def calculate_optimal_hedge_ratio_and_cadfs(ts1: list, ts2: list):
    """
    Calculate the optimal hedge ratio (beta) and perform the CADF (Cointegrated Augmented Dickey-Fuller) test on the residuals.

    This function takes two time series as input, computes the optimal hedge ratio by fitting a linear regression model, 
    and then performs the CADF test on the residuals to check for cointegration.

    Parameters:
        ts1 (list): List containing the first time series data.
        ts2 (list): List containing the second time series data.

    Returns:
        dict: A dictionary containing:
            - 'beta_hr' (float): The optimal hedge ratio.
            - 'cadf' (tuple): The results of the CADF test on the residuals.
    """
    
    # Convert the lists to numpy arrays
    ts1_array = np.array(ts1)
    ts2_array = np.array(ts2)
    
    # Ensure the time series have the same length by trimming the longer series
    min_length = min(len(ts1_array), len(ts2_array))
    ts1_array = ts1_array[:min_length]
    ts2_array = ts2_array[:min_length]
    
    # Reshape ts1 for regression
    ts1_array = ts1_array.reshape(-1, 1)
    
    # Calculate optimal hedge ratio (beta)
    regression_result = OLS(ts2_array, ts1_array).fit()
    beta_hr = regression_result.params[0]

    # Calculate the residuals of the linear combination
    residuals = ts2_array - beta_hr * ts1_array.flatten()

    # Perform the CADF test on the residuals
    cadf_result = adfuller(residuals)

    return {
        "beta_hr": beta_hr,
        "cadf": cadf_result
    }


def calculate_hurst_exponents(ts: list):
    """
    Calculate the Hurst exponent of a time series.

    Parameters:
    ts (list): A list representing the time series data.

    Returns:
    float: The Hurst exponent of the time series. Returns NaN if the time series is too short 
           or if the computation fails.
    """

    ts = np.log(np.cumsum(ts))

    lags = range(2, 100)
    tau = []

    for lag in lags:
        if len(ts) <= lag:
            break

        lagged_diff = ts[lag:] - ts[:-lag]
        if len(lagged_diff) > 1:
            tau.append(np.std(lagged_diff))

    tau = np.array(tau)

    # Filter out invalid (zero or NaN) tau values
    valid = (tau > 0)
    lags = np.array(lags[:len(tau)])[valid]
    tau = tau[valid]

    if len(tau) < 2:
        return np.nan

    # Perform linear regression on log-log scale
    poly = np.polyfit(np.log(lags), np.log(tau), 1)
    
    hurstcomponent =  poly[0] * 2.0
    
    return {
        "hurstcomponent": hurstcomponent,
    }



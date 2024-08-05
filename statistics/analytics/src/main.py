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
    # Simulate processing the message (e.g., appending a response)
    ts1 = [70773.64, 69394, 69304.05, 69649.9, 69497.73, 67316.53, 68248.6, 66756.5, 66004.39, 66192, 66481.81, 65152.8, 64943.79, 64841.46, 64087.9, 64235.01, 63171.43, 64253, 60815.1, 61615.39, 60313.35, 60860, 62668.26, 62830.13, 62039.45, 56639.43, 58244.75, 55854.09, 57230.64, 57230.64, 55649.8, 57230.64] 
    ts2 = [3812.09, 3676.69, 3680.84, 3706.26, 3665.86, 3497.31, 3559.14, 3467.65, 3479.53, 3566.69, 3622.1, 3509.81, 3482.06, 3559.14, 3510.73, 3517.19, 3494.09, 3418.42, 3350.59, 3393.6, 3369.31, 3445.58, 3373.62, 3373.26, 3432.37, 3438.36, 3416.17, 3291.74, 3058.89, 2981.74, 3067.39, 2930.78]

    # Calculate ADF test results
    adf_results = calculate_optimal_hedge_ratio_and_cadf(ts1, ts2)

    # Prepare the processed message with the results
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
    return {"response": processed_message}
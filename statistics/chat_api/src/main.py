from fastapi import FastAPI

app = FastAPI()

@app.get("/helloword")
def read_root():
    print("Hello from FastAPI inside Docker!")
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    print(f"Fetching item with id: {item_id} and query: {q}")
    return {"item_id": item_id, "q": q}


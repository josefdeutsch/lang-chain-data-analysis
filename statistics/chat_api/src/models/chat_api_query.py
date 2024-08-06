from pydantic import BaseModel

class ChatApiQueryInput(BaseModel):
    text: str


class ChatApiOutput(BaseModel):
    input: str
    output: str
    intermediate_steps: list[str]

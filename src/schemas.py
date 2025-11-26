from pydantic import BaseModel
from typing_extensions import List


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str = "gpt-4o"
    messages: List[Message]
    temperature: float = 0.7

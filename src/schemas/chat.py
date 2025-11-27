from pydantic import BaseModel
from typing import List, Optional


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    id: int
    model: str = "gpt-4o"
    messages: List[Message]
    temperature: float = 0.7

    

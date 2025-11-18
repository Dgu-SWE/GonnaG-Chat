import os
import httpx
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from openai import AsyncOpenAI

BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("OPEN_API_KEY")
if not API_KEY:
    raise ValueError("OPEN_API_KEY 설정 없음")

client = AsyncOpenAI(api_key=API_KEY)
app = FastAPI()


async def fetch_mcp_data():
    spring_url = "http://localhost:8080/mcp"
    try:
        async with httpx.AsyncClient() as http_client:
            response = await http_client.get(spring_url)
            response.raise_for_status()

            return response.text

    except Exception as e:
        return f"백엔드 서버 통신 에러 : {str(e)}"


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_mcp_info",
            "description": "MCP 프로젝트의 현재 상태나 생성 정보를 조회합니다. 사용자가 MCP에 대해 물어볼 때 사용하세요.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    }
]


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str = "gpt-4o"
    messages: List[Message]
    temperature: float = 0.7


@app.post("/chat")
async def generate_chat_response(request: ChatRequest):
    try:
        response = await client.chat.completions.create(
            model=request.model,
            messages=[msg.model_dump() for msg in request.messages],
            temperature=request.temperature,
            tools=tools,
            tool_choice="auto",
        )

        response_message = response.choices[0].message

        tool_calls = response_message.tool_calls
        if tool_calls:
            messages = [msg.model_dump(exclude_none=True) for msg in request.messages]
            messages.append(response_message)

            for tool_call in tool_calls:
                if tool_call.function.name == "get_mcp_info":
                    function_response = await fetch_mcp_data()

                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": "get_mcp_info",
                            "content": function_response,
                        }
                    )

        final_response = await client.chat.completions.create(
            model=request.model, messages=messages
        )

        return {
            "role": "assistant",
            "content": final_response.choices[0].message.content,
        }
    except Exception as e:
        print(f"Error : {e}")
        raise HTTPException(status_code=500, detail=str(e))

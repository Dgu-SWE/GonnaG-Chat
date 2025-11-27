from fastapi import APIRouter, HTTPException
from src.schemas import ChatRequest
from src.agent import process_user_query

router = APIRouter(prefix="/api")


@router.post("/chat")
async def generate_resposne(request: ChatRequest):
    try:
        user_query = request.messages[-1].content
        response_content = await process_user_query(user_query)

        return {"role": "assistant", "content": response_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

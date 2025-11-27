from fastapi import APIRouter, HTTPException
from src.schemas.chat import ChatRequest
from src.agents.orchestrator import process_user_query

router = APIRouter(prefix="/api")


@router.post("/chat")
async def generate_response(request: ChatRequest):
    try:
        user_query = request.messages

        reponse_content = await process_user_query(
            user_query=user_query, user_id=request.user_id
        )

        return {"role": "assistnt", "content": reponse_content}
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

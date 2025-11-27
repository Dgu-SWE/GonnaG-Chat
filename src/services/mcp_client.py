import httpx
from src.config import SPRING_BASE_URL


async def test_mcp():
    """mcp 테스트용 함수"""

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(SPRING_BASE_URL + "/mcp")
            response.raise_for_status()
            return response.text

    except Exception as e:
        return f"테스트 실패 {str(e)}"


async def _post(endpoint: str, id: int) -> str:
    """내부 공통 POST 요청 함수"""
    url = f"{SPRING_BASE_URL}{endpoint}"
    payload = {"id": id}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=10.0)
            response.raise_for_status()
            return response.text

    except Exception as e:
        return f"데이터 조회 실패 {str(e)}"


async def fetch_announcements(id: int):
    return await _post("/mcp/announcements", id)


async def fetch_user_info(id: int):
    return await _post("/mcp/user-info", id)


async def fetch_class_info(id: int):
    return await _post("/mcp/classes", id)


async def fetch_academic_guide(id: int):
    return await _post("/mcp/guide", id)

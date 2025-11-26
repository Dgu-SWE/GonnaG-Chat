import httpx


async def get_mcp_data() -> str:
    get_mcp_url = "http://localhost:8080/mcp"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(get_mcp_url, timeout=5.0)
            response.raise_for_status()
            return response.text
    except Exception as e:
        return f"데이터 조회 실패: {str(e)}"

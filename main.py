from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(title="나도 졸업할래 챗봇서버")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, reload_dirs=["src"])

from fastapi import APIRouter
from openai import AsyncOpenAI
from schemas import ChatRequest

router = APIRouter(prefix="/api")


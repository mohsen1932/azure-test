from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.dependencies import get_langchain_service
from app.services.langchain_service import LangChainService

router = APIRouter()


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    response: str


class HealthResponse(BaseModel):
    status: str


@router.get("/health")
async def health() -> HealthResponse:
    return HealthResponse(status="healthy")


@router.post("/chat")
async def chat(
    request: ChatRequest,
    service: Annotated[LangChainService, Depends(get_langchain_service)],
) -> ChatResponse:
    result = await service.invoke(request.message)
    return ChatResponse(response=result)

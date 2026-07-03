from fastapi import APIRouter

from app.schemas.assistant import (
    AssistantRequest,
    AssistantResponse,
)

from app.services.rag_service import rag_service


router = APIRouter(
    tags=["AI Assistant"]
)


@router.post(
    "/assistant",
    response_model=AssistantResponse,
)
def ask(request: AssistantRequest):

    result = rag_service.generate_answer(

        question=request.question,

        history=request.history

    )

    return AssistantResponse(
        answer=result["answer"],
        source_type=result["source_type"],
        sources=result["sources"],
        similarity_score=result["similarity_score"],
        confidence=result["confidence"],
    )
from typing import List

from pydantic import BaseModel


class ChatMessage(BaseModel):

    role: str

    content: str


class AssistantRequest(BaseModel):

    question: str

    history: List[ChatMessage] = []


class AssistantResponse(BaseModel):

    answer: str

    source_type: str

    sources: List[str]

    similarity_score: float | None = None

    confidence: float | None = None
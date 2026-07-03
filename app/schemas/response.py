from pydantic import BaseModel


class PredictionResponse(BaseModel):
    predicted_productivity: float
    unit: str

    land_area: float
    estimated_yield_quintal: float
    estimated_yield_ton: float


class AssistantResponse(BaseModel):
    answer: str
    sources: list[str]
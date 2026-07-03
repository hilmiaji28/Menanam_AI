from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    kabupaten: str = Field(..., example="Bandung")
    komoditas: str = Field(..., example="Padi")

    luas_lahan: float = Field(
        ...,
        gt=0,
        example=2.5,
        description="Luas lahan dalam hektar"
    )

    temperature: float
    temp_max: float
    temp_min: float
    rainfall: float
    humidity: float
    wind_speed: float
    solar_radiation: float


class PredictionResponse(BaseModel):
    predicted_productivity: float
    unit: str

    land_area: float
    estimated_yield_quintal: float
    estimated_yield_ton: float
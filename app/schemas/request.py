from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    kabupaten: str = Field(..., example="Bandung")
    komoditas: str = Field(..., example="Padi")

    temperature: float = Field(..., example=27.5)
    temp_max: float = Field(..., example=31.2)
    temp_min: float = Field(..., example=22.3)

    rainfall: float = Field(..., example=8.5)
    humidity: float = Field(..., example=81)

    wind_speed: float = Field(..., example=2.4)
    solar_radiation: float = Field(..., example=17.8)


class AssistantRequest(BaseModel):
    question: str = Field(
        ...,
        example="Bagaimana cara mengatasi penyakit blas pada padi?"
    )
from fastapi import APIRouter, HTTPException

from app.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
)

from app.services.predictor import prediction_service

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"],
)


@router.post(
    "",
    response_model=PredictionResponse,
)
def predict(request: PredictionRequest):

    try:

        predicted_productivity = prediction_service.predict(
            request.model_dump()
        )

        estimated_quintal = (
            predicted_productivity * request.luas_lahan
        )

        estimated_ton = estimated_quintal / 10

        return PredictionResponse(
            predicted_productivity=round(predicted_productivity, 2),
            unit="kuintal/ha",
            land_area=request.luas_lahan,
            estimated_yield_quintal=round(estimated_quintal, 2),
            estimated_yield_ton=round(estimated_ton, 2),
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
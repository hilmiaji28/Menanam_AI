from fastapi import APIRouter

from app.services.loader import model_loader

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("")
def health():

    return {

        "status": "healthy",

        "prediction_model":

            model_loader.get_model() is not None,

        "embedding":

            model_loader.get_embedding() is not None,

        "vector_db":

            model_loader.get_vector_db() is not None,

        "retriever":

            model_loader.get_retriever() is not None

    }
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.predict import router as predict_router
from app.api.rag import router as rag_router

from app.services.loader import model_loader


@asynccontextmanager
async def lifespan(app: FastAPI):

    model_loader.load_model()

    model_loader.load_embedding()

    model_loader.load_vector_db()

    model_loader.load_retriever()

    yield


app = FastAPI(
    title="Menanam AI API",
    version="1.0.0",
    description="AI-powered crop productivity prediction and agricultural assistant.",
    lifespan=lifespan
)

app.include_router(health_router)
app.include_router(predict_router)
app.include_router(rag_router)
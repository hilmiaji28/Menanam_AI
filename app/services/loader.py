import joblib

from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from app.core.config import (
    MODEL_PATH,
    EMBEDDING_MODEL,
    VECTOR_DB_PATH,
    TOP_K,
    FETCH_K,
)


class ModelLoader:

    def __init__(self):

        self.model = None

        self.embedding = None

        self.vector_db = None

        self.retriever = None

    # =====================================================

    def load_model(self):

        print("MODEL PATH:", MODEL_PATH)

        print("EXISTS:", Path(MODEL_PATH).exists())

        if self.model is None:

            print("Loading Prediction Model...")

            self.model = joblib.load(MODEL_PATH)

            print("Prediction Model Loaded")

    def get_model(self):

        return self.model

    # =====================================================

    def load_embedding(self):

        if self.embedding is None:

            print("Loading Embedding...")

            self.embedding = HuggingFaceEmbeddings(
                model_name=EMBEDDING_MODEL,
                model_kwargs={
                    "device": "cpu"
                },
                encode_kwargs={
                    "normalize_embeddings": True
                }
            )

            print("Embedding Loaded")

    def get_embedding(self):

        return self.embedding

    # =====================================================

    def load_vector_db(self):

        if self.embedding is None:

            raise RuntimeError(
                "Embedding belum dimuat."
            )

        if self.vector_db is None:

            print("Loading ChromaDB...")

            self.vector_db = Chroma(
                persist_directory=str(VECTOR_DB_PATH),
                embedding_function=self.embedding,
            )

            print("ChromaDB Loaded")

    def get_vector_db(self):

        return self.vector_db

    # =====================================================

    def load_retriever(self):

        if self.vector_db is None:

            raise RuntimeError(
                "Vector DB belum dimuat."
            )

        if self.retriever is None:

            self.retriever = self.vector_db.as_retriever(
                search_type="mmr",
                search_kwargs={
                    "k": TOP_K,
                    "fetch_k": FETCH_K,
                }
            )

            print("Retriever Loaded")

    def get_retriever(self):

        return self.retriever


model_loader = ModelLoader()
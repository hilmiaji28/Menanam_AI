from langchain_chroma import Chroma

from .embeddings import get_embeddings


def get_vectordb():

    return Chroma(
        persist_directory="vector_db/chroma",
        embedding_function=get_embeddings(),
    )
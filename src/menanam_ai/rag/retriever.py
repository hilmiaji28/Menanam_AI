"""
=========================================================

Retriever

Embedding
    ↓
ChromaDB
    ↓
MMR Search
    ↓
Top-k Documents

=========================================================
"""

from .vectordb import get_vectordb


class CropRetriever:
    """
    Menanam-AI Retriever

    Retrieval Method:
        - ChromaDB
        - MMR
        - multilingual-e5-base
    """

    def __init__(
        self,
        k: int = 5,
        fetch_k: int = 20,
        lambda_mult: float = 0.7,
    ):

        self.db = get_vectordb()

        self.retriever = self.db.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": k,
                "fetch_k": fetch_k,
                "lambda_mult": lambda_mult,
            },
        )

    def retrieve(self, question: str):
        """
        Retrieve relevant documents.

        Parameters
        ----------
        question : str

        Returns
        -------
        list[Document]
        """

        query = f"query: {question}"

        documents = self.retriever.invoke(query)

        return documents
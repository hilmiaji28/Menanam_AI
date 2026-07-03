"""
=========================================================

RAG Tool

Tool untuk menjawab pertanyaan budidaya tanaman
menggunakan Knowledge Base (RAG).

=========================================================
"""

from menanam_ai.core.logger import get_logger
from menanam_ai.core.response import ResponseBuilder

from ..rag.assistant import CropAssistant


logger = get_logger(__name__)


class RagTool:

    def __init__(self, llm):

        self.assistant = CropAssistant(llm)

    # =====================================================
    # Run
    # =====================================================

    def run(self, question: str):

        logger.info(f"RAG Tool | Question: {question}")

        try:

            result = self.assistant.ask(question)

            logger.info(
                f"RAG Tool | Retrieved {result.get('documents', 0)} documents"
            )

            return ResponseBuilder.success(

                tool="rag",

                intent="budidaya",

                answer=result.get("answer"),

                question=question,

                sources=result.get("sources", []),

                documents=result.get("documents", 0),

                retrieved_crop=result.get("retrieved_crop"),

            )

        except Exception as e:

            logger.error(f"RAG Tool Error : {e}")

            error_message = str(e)

            # ---------------------------------------------
            # Gemini quota exceeded
            # ---------------------------------------------

            if "RESOURCE_EXHAUSTED" in error_message:

                return ResponseBuilder.error(

                    tool="rag",

                    intent="budidaya",

                    status="quota_exceeded",

                    answer=(
                        "Knowledge base berhasil ditemukan, "
                        "namun AI sedang tidak dapat menyusun jawaban "
                        "karena kuota layanan LLM telah habis. "
                        "Silakan coba kembali beberapa saat lagi."
                    ),

                    error=error_message,

                    question=question,

                    sources=[],

                    documents=0,

                    retrieved_crop=None,

                )

            # ---------------------------------------------
            # General Error
            # ---------------------------------------------

            return ResponseBuilder.error(

                tool="rag",

                intent="budidaya",

                answer=(
                    "Maaf, terjadi kesalahan saat mengakses "
                    "knowledge base."
                ),

                error=error_message,

                question=question,

                sources=[],

                documents=0,

                retrieved_crop=None,

            )
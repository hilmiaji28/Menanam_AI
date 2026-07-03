from langchain_core.tracers import context
from IPython.core import getipython
import logging

from app.core.config import (
    TOP_K,
    SIMILARITY_THRESHOLD,
    TOP_SCORE_MARGIN,
    MAX_CONTEXT_LENGTH,
    MAX_HISTORY,
)

from app.services.loader import model_loader
from app.services.llm import llm
from app.services.internet_search import internet_search
from app.services.prompt import RAG_PROMPT
from app.services.retrieval_utils import detect_filter

logger = logging.getLogger(__name__)


class RAGService:

    # =====================================================
    # RETRIEVE DOCUMENTS
    # =====================================================

    def retrieve(self, question: str):

        vector_db = model_loader.get_vector_db()

        if vector_db is None:
            raise RuntimeError("Vector DB belum dimuat.")

        query = f"query: {question}"

        filter_metadata = detect_filter(question)

        results = vector_db.similarity_search_with_score(
            query=query,
            k=TOP_K,
            filter=filter_metadata
        )

        docs = []
        scores = []

        logger.info("=" * 80)
        logger.info("RETRIEVAL RESULT")
        logger.info("=" * 80)

        for doc, score in results:

            docs.append(doc)
            scores.append(score)

            logger.info(
                f"{score:.4f} | {doc.metadata.get('source')}"
            )

        return docs, scores

    # =====================================================
    # FILTER DOCUMENTS
    # =====================================================

    def filter_documents(
        self,
        docs,
        scores,
    ):

        if len(scores) == 0:

            return []

        best_score = min(scores)

        filtered = []

        for doc, score in zip(docs, scores):

            if score <= best_score + TOP_SCORE_MARGIN:

                filtered.append(doc)

        logger.info(
            f"Filtered {len(filtered)} / {len(docs)} documents"
        )

        return filtered

    # =====================================================
    # SHOULD FALLBACK
    # =====================================================

    def should_fallback(self, scores):

        if len(scores) == 0:

            logger.warning("No document retrieved.")

            return True

        best_score = min(scores)

        logger.info(
            f"Best Score : {best_score:.4f}"
        )

        logger.info(
            f"Threshold  : {SIMILARITY_THRESHOLD:.4f}"
        )

        fallback = (
            best_score > SIMILARITY_THRESHOLD
        )

        logger.info(
            f"Fallback   : {fallback}"
        )

        return fallback

    # =====================================================
    # BUILD CONTEXT
    # =====================================================

    def build_context(
        self,
        docs,
    ):

        cleaned_docs = []

        for doc in docs:

            text = doc.page_content.replace(
                "passage: ",
                ""
            )

            cleaned_docs.append(text)

        context = "\n\n".join(cleaned_docs)

        context = context[:MAX_CONTEXT_LENGTH]

        return context

    # =====================================================
    # BUILD HISTORY
    # =====================================================

    def build_history(
        self,
        history,
    ):

        if not history:

            return ""

        conversations = []

        for chat in history[-MAX_HISTORY:]:

            role = chat.role.capitalize()

            conversations.append(
                f"{role}: {chat.content}"
            )

        return "\n".join(conversations)

    # =====================================================
    # KNOWLEDGE BASE SOURCES
    # =====================================================

    def get_sources(
        self,
        docs,
    ):

        sources = []

        for doc in docs:

            source = doc.metadata.get(
                "source"
            )

            if (
                source
                and source not in sources
            ):

                sources.append(source)

        return sources

    # =====================================================
    # INTERNET SEARCH
    # =====================================================

    def internet_context(
        self,
        question,
    ):

        try:

            response = internet_search.search(
                question
            )

            context = ""

            sources = []

            for item in response["results"]:

                context += (
                    item["content"] + "\n\n"
                )

                sources.append(
                    item["url"]
                )

            return context, sources

        except Exception as e:

            logger.exception(e)

            return "", []

        # =====================================================
    # GENERATE FINAL ANSWER
    # =====================================================

    def generate_answer(
        self,
        question: str,
        history=None,
    ):

        # ---------------------------------------------
        # Retrieve
        # ---------------------------------------------

        docs, scores = self.retrieve(question)

        best_score = min(scores) if scores else None

        fallback = self.should_fallback(scores)

        # ---------------------------------------------
        # Filter Documents
        # ---------------------------------------------

        docs = self.filter_documents(
            docs,
            scores,
        )

        # ---------------------------------------------
        # Build Context
        # ---------------------------------------------

        history_text = self.build_history(history)

        if fallback:

            logger.info(
                "Using Internet Search..."
            )

            context, sources = self.internet_context(
                question
            )

            source_type = "internet"

            if context.strip() == "":

                context = (
                    "Tidak ditemukan informasi "
                    "yang relevan dari Internet."
                )

        else:

            logger.info(
                "Using Knowledge Base..."
            )

            context = self.build_context(
                docs
            )

            sources = self.get_sources(
                docs
            )

            source_type = "knowledge_base"

        # ---------------------------------------------
        # Build Prompt
        # ---------------------------------------------

        prompt = RAG_PROMPT.format(
            history=history_text,
            context=context,
            question=question,
        )

        # ---------------------------------------------
        # Generate Answer
        # ---------------------------------------------

        try:

            response = llm.invoke(prompt)

            answer = response.content

        except Exception as e:

            logger.exception(e)

            error = str(e)

            # ==================================================
            # FALLBACK KE KNOWLEDGE BASE
            # ==================================================

            if source_type == "knowledge_base" and context.strip():

                answer = (
                    "⚠️ AI sedang tidak tersedia. "
                    "Berikut informasi yang ditemukan dari Knowledge Base.\n\n"
                    f"{context}"
                )

            elif source_type == "internet" and context.strip():

                answer = (
                    "⚠️ AI sedang tidak tersedia. "
                    "Berikut informasi yang ditemukan dari Internet.\n\n"
                    f"{context}"
                )

            elif (
                "RESOURCE_EXHAUSTED" in error
                or "429" in error
            ):

                answer = (
                    "Maaf, kuota layanan AI sedang habis. "
                    "Silakan coba beberapa saat lagi."
                )

            elif (
                "Deadline" in error
                or "Timeout" in error
            ):

                answer = (
                    "Permintaan membutuhkan waktu terlalu lama."
                )

            else:

                answer = (
                    "Terjadi kesalahan saat menghasilkan jawaban."
                )

        # ---------------------------------------------
        # Confidence
        # ---------------------------------------------

        confidence = None

        if best_score is not None:

            confidence = round(
                max(
                    0.0,
                    (1 - best_score) * 100,
                ),
                1,
            )

        # ---------------------------------------------
        # Logging
        # ---------------------------------------------

        logger.info("=" * 80)

        logger.info(
            f"Source Type : {source_type}"
        )

        logger.info(
            f"Similarity  : {best_score}"
        )

        logger.info(
            f"Confidence  : {confidence}"
        )

        logger.info(
            f"Sources      : {sources}"
        )

        logger.info("=" * 80)

        # ---------------------------------------------
        # Final Response
        # ---------------------------------------------

        return {

            "answer": answer,

            "source_type": source_type,

            "sources": sources,

            "similarity_score": (
                round(best_score, 4)
                if best_score is not None
                else None
            ),

            "confidence": confidence,

        }


rag_service = RAGService()        
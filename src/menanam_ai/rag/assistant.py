"""
=========================================================

Menanam-AI Assistant

Flow

User Question
        │
        ▼
Retriever (MMR)
        │
        ▼
Top-k Documents
        │
        ▼
Format Context
        │
        ▼
Gemini
        │
        ▼
Answer + Sources

=========================================================
"""

from .prompt import SYSTEM_PROMPT
from .retriever import CropRetriever

class CropAssistant:

    def __init__(self, llm):
        """
        Parameters
        ----------
        llm : LangChain Chat Model
        """

        self.llm = llm
        self.retriever = CropRetriever()

    # =====================================================
    # Build Context
    # =====================================================

    def _build_context(self, documents):

        contexts = []

        for i, doc in enumerate(documents, start=1):

            content = doc.page_content.strip()

            if content.startswith("passage:"):
                content = content.replace("passage:", "", 1).strip()

            contexts.append(
f"""
=== Document {i} ===

Crop      : {doc.metadata.get("crop", "-")}
Category  : {doc.metadata.get("category", "-")}
Source    : {doc.metadata.get("source", "-")}

Content:
{content}
"""
            )

        return "\n".join(contexts)

    # =====================================================
    # Deduplicate Sources
    # =====================================================

    def _build_sources(self, documents):

        sources = []
        seen = set()

        for doc in documents:

            source = doc.metadata.get("source")

            if source in seen:
                continue

            seen.add(source)

            sources.append(
                {
                    "crop": doc.metadata.get("crop"),
                    "category": doc.metadata.get("category"),
                    "source": source,
                }
            )

        return sources

    # =====================================================
    # Ask Assistant
    # =====================================================

    def ask(self, question: str):

        # --------------------------------------------
        # Retrieve Documents
        # --------------------------------------------

        documents = self.retriever.retrieve(question)

        # --------------------------------------------
        # Build Context
        # --------------------------------------------

        context = self._build_context(documents)

        # --------------------------------------------
        # Prompt
        # --------------------------------------------

        prompt = f"""
        {SYSTEM_PROMPT}

==================================================

Context

{context}

==================================================

Pertanyaan

{question}

==================================================

Jawablah berdasarkan Context di atas.

Aturan:

1. Gunakan HANYA informasi pada Context.
2. Jangan mengarang jawaban.
3. Jika informasi tidak tersedia,
   katakan bahwa informasi tersebut
   tidak ada pada knowledge base.
4. Jawab dalam Bahasa Indonesia.
5. Gunakan bahasa yang sederhana.
6. Bila memungkinkan gunakan poin-poin.
"""

        # --------------------------------------------
        # LLM
        # --------------------------------------------

        response = self.llm.invoke(prompt)

        # --------------------------------------------
        # Sources
        # --------------------------------------------

        sources = self._build_sources(documents)

        # --------------------------------------------
        # Crop Retrieved
        # --------------------------------------------

        retrieved_crop = None

        if documents:
            retrieved_crop = documents[0].metadata.get("crop")

        # --------------------------------------------
        # Return
        # --------------------------------------------

        return {
            "question": question,
            "answer": response.content,
            "sources": sources,
            "documents": len(documents),
            "retrieved_crop": retrieved_crop,
        }
from .embedding import get_embedding_model
from .retriever import load_retriever
from .assistant import MenanamAIAssistant


class MenanamAIChatbot:

    def __init__(self):

        # Load embedding model
        self.embedding = get_embedding_model()

        # Load retriever
        self.retriever = load_retriever(
            self.embedding
        )

        # Load Gemini assistant
        self.assistant = MenanamAIAssistant()

    def ask(self, question: str):

        # =====================================
        # Retrieve relevant documents
        # =====================================

        docs = self.retriever.invoke(question)

        if len(docs) == 0:

            return {
                "answer": "Informasi belum tersedia pada knowledge base lokal.",
                "sources": [],
                "confidence": 0.0,
                "fallback_used": True,
            }
        
        print("=" * 80)
        print("JUMLAH DOKUMEN:", len(docs))

        for i, doc in enumerate(docs, 1):
            print("=" * 80)
            print(f"Rank {i}")
            print(doc.metadata)
            print(doc.page_content[:500])

        # =====================================
        # Build context
        # =====================================

        context = "\n\n".join(
            doc.page_content
            for doc in docs
        )

        # =====================================
        # Build source metadata
        # =====================================

        sources = []

        for doc in docs:

            source = {
                "file": doc.metadata.get(
                    "source",
                    ""
                ).split("\\")[-1],

                "page": doc.metadata.get(
                    "page_label",
                    doc.metadata.get("page", "")
                )
            }

            # Hindari duplikasi
            if source not in sources:
                sources.append(source)

        # =====================================
        # Generate answer
        # =====================================

        answer = self.assistant.generate(
            question=question,
            context=context
        )

        # =====================================
        # Final response
        # =====================================

        return {

            "answer": answer,

            "sources": sources,

            # nanti kita ganti menggunakan similarity score
            "confidence": None,

            # nanti dipakai Academic Search
            "fallback_used": False,
        }
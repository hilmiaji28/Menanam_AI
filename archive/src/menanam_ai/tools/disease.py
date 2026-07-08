"""
=========================================================

Disease Tool

Mencari informasi penyakit tanaman menggunakan Tavily
kemudian menyusun jawaban menggunakan LLM.

=========================================================
"""

import os

from tavily import TavilyClient

from menanam_ai.core.logger import get_logger
from menanam_ai.core.response import ResponseBuilder

logger = get_logger(__name__)


class DiseaseTool:

    def __init__(self, llm):

        self.llm = llm

        self.client = TavilyClient(
            api_key=os.getenv("TAVILY_API_KEY")
        )

    # =====================================================
    # Run
    # =====================================================

    def run(self, question: str):

        logger.info(f"Disease Tool | Question: {question}")

        try:

            # ---------------------------------------------
            # Search Tavily
            # ---------------------------------------------

            search = self.client.search(

                query=question,

                search_depth="advanced",

                max_results=5,

            )

            results = search.get("results", [])

            logger.info(
                f"Disease Tool | Retrieved {len(results)} results"
            )

            # ---------------------------------------------
            # No Result
            # ---------------------------------------------

            if len(results) == 0:

                return ResponseBuilder.error(

                    tool="disease",

                    intent="penyakit",

                    answer=(
                        "Maaf, saya tidak menemukan informasi "
                        "yang relevan mengenai penyakit tersebut."
                    ),

                    error="No search results",

                    question=question,

                    sources=[],

                )

            # ---------------------------------------------
            # Build Context
            # ---------------------------------------------

            context = ""

            for i, item in enumerate(results, start=1):

                context += f"""

=== Source {i} ===

Title:
{item['title']}

Content:
{item['content']}

"""

            prompt = f"""
Anda adalah AI Assistant bidang pertanian.

Gunakan informasi berikut untuk menjawab pertanyaan pengguna.

{context}

==================================================

Pertanyaan:

{question}

==================================================

Jawablah dalam Bahasa Indonesia.

Gunakan poin-poin jika memungkinkan.

Jika informasi kurang lengkap,
katakan dengan jujur.
"""

            # ---------------------------------------------
            # LLM
            # ---------------------------------------------

            response = self.llm.invoke(prompt)

            sources = [

                {

                    "title": item["title"],

                    "url": item["url"],

                }

                for item in results

            ]

            return ResponseBuilder.success(

                tool="disease",

                intent="penyakit",

                answer=response.content,

                question=question,

                sources=sources,

                retrieved=len(results),

            )

        # =================================================
        # Error Handling
        # =================================================

        except Exception as e:

            error_message = str(e)

            logger.error(
                f"Disease Tool Error : {error_message}"
            )

            # ---------------------------------------------
            # Quota Gemini
            # ---------------------------------------------

            if "RESOURCE_EXHAUSTED" in error_message:

                try:

                    sources = [

                        {

                            "title": item["title"],

                            "url": item["url"],

                        }

                        for item in results

                    ]

                except Exception:

                    sources = []

                return ResponseBuilder.error(

                    tool="disease",

                    intent="penyakit",

                    status="quota_exceeded",

                    answer=(
                        "Informasi penyakit berhasil ditemukan dari internet, "
                        "namun AI tidak dapat menyusun jawaban karena "
                        "kuota layanan LLM telah habis. "
                        "Silakan coba kembali beberapa saat lagi."
                    ),

                    error=error_message,

                    question=question,

                    sources=sources,

                    retrieved=len(sources),

                )

            # ---------------------------------------------
            # General Error
            # ---------------------------------------------

            return ResponseBuilder.error(

                tool="disease",

                intent="penyakit",

                answer=(
                    "Terjadi kesalahan saat mencari informasi "
                    "penyakit tanaman."
                ),

                error=error_message,

                question=question,

                sources=[],

                retrieved=0,

            )
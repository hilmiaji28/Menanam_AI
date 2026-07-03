"""
=========================================================

Tavily Search Service

Digunakan untuk mencari informasi terbaru
dari internet.

=========================================================
"""

import os

from tavily import TavilyClient


class TavilySearchService:

    def __init__(self):

        api_key = os.getenv("TAVILY_API_KEY")

        if not api_key:
            raise ValueError(
                "TAVILY_API_KEY not found."
            )

        self.client = TavilyClient(api_key=api_key)

    # =====================================================

    def search(
        self,
        query: str,
        max_results: int = 5,
    ):

        response = self.client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced",
        )

        return response
from tavily import TavilyClient

from app.core.config import (
    TAVILY_API_KEY,
    MAX_SEARCH_RESULTS,
)


client = TavilyClient(
    api_key=TAVILY_API_KEY
)


class InternetSearchService:

    def search(
        self,
        question: str,
        max_results: int = MAX_SEARCH_RESULTS,
    ):

        response = client.search(
            query=question,
            search_depth="advanced",
            max_results=max_results,
        )

        return response


internet_search = InternetSearchService()
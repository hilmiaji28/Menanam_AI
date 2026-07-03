from dotenv import load_dotenv

from menanam_ai.services.tavily_search import TavilySearchService

load_dotenv()

service = TavilySearchService()

result = service.search(
    "cara mengatasi penyakit blast pada padi"
)

print("=" * 100)
print(result)
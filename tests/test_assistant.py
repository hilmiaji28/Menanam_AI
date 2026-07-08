from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from menanam_ai.rag.assistant import CropAssistant

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
)

assistant = CropAssistant(llm)

questions = [
    "Bagaimana cara pemupukan padi?",
    "Kapan panen jagung?",
    "Bagaimana pengolahan lahan singkong?"
]

for q in questions:

    result = assistant.ask(q)

    print("=" * 100)
    print("QUESTION")
    print("=" * 100)
    print(result["question"])

    print()

    print("=" * 100)
    print("ANSWER")
    print("=" * 100)
    print(result["answer"])

    print()

    print("=" * 100)
    print("SOURCES")
    print("=" * 100)

    for s in result["sources"]:
        print(s)

    print()
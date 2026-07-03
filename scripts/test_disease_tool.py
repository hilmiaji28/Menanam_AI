from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from menanam_ai.tools.disease import DiseaseTool

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
)

tool = DiseaseTool(llm)

questions = [

    "Bagaimana cara mengatasi penyakit blast pada padi?",

    "Apa penyebab bulai pada jagung?",

    "Bagaimana mengendalikan busuk batang singkong?"

]

for question in questions:

    print("=" * 100)
    print("QUESTION")
    print("=" * 100)
    print(question)

    result = tool.run(question)

    print()

    print("=" * 100)
    print("ANSWER")
    print("=" * 100)
    print(result["answer"])

    print()

    print("=" * 100)
    print("SOURCES")
    print("=" * 100)

    for source in result["sources"]:
        print(source)

    print()
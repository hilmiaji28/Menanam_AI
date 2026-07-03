"""
=========================================================

Test Router

=========================================================
"""

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from menanam_ai.router.router import Router

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
)

router = Router(llm)

questions = [

    # Budidaya
    "Bagaimana cara pemupukan padi?",
    "Bagaimana jarak tanam jagung?",
    "Kapan panen jagung?",
    "Bagaimana pengolahan lahan singkong?",
    "Bagaimana memilih benih padi?",

    # Penyakit
    "Daun padi saya terkena blast",
    "Jagung saya terkena bulai",
    "Singkong saya layu",
    "Apa penyebab busuk batang jagung?",
    "Pestisida apa yang cocok?",

    # Prediction
    "Prediksi hasil panen jagung",
    "Estimasi hasil panen saya",
    "Hitung produktivitas lahan",

    # Recommendation
    "Tanaman apa yang cocok ditanam?",
    "Rekomendasikan tanaman terbaik",

    # Ambiguous (akan memakai LLM)
    "Saya baru tanam padi umur 15 hari dan sekarang tumbuh lambat.",
    "Saya ingin mulai bertani.",

    # Unknown
    "Siapa presiden Indonesia?",
]

print("=" * 100)
print("MENANAM-AI ROUTER TEST")
print("=" * 100)

for i, question in enumerate(questions, start=1):

    result = router.route(question)

    print(f"\n[{i}]")
    print(f"Question   : {question}")
    print(f"Intent     : {result['intent']}")
    print(f"Method     : {result['method']}")
    print(f"Confidence : {result['confidence']}")

print("\n" + "=" * 100)
print("Router Test Finished")
print("=" * 100)
"""
=========================================================

Menanam-AI Agent Test

=========================================================
"""

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from menanam_ai.agent.agent import Agent

load_dotenv()

# =====================================================
# LLM
# =====================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
)

agent = Agent(llm)

# =====================================================
# Test Cases
# =====================================================

tests = [

    # ---------------- RAG ----------------

    {
        "question": "Bagaimana cara pemupukan padi?",
        "kwargs": {}
    },

    {
        "question": "Kapan panen jagung?",
        "kwargs": {}
    },

    # ---------------- Disease ----------------

    {
        "question": "Bagaimana mengatasi penyakit blast pada padi?",
        "kwargs": {}
    },

    # ---------------- Prediction ----------------

    {
        "question": "Prediksi hasil panen padi",

        "kwargs": {

            "crop": "Padi",

            "temperature": 27,

            "temp_max": 31,

            "temp_min": 24,

            "rainfall": 220,

            "humidity": 82,

            "wind_speed": 2,

            "solar_radiation": 18,

            "land_area": 2.5,

        }

    },

    # ---------------- Recommendation ----------------

    {
        "question": "Tanaman apa yang cocok ditanam?",

        "kwargs": {

            "N": 90,

            "P": 42,

            "K": 43,

            "temperature": 27,

            "humidity": 82,

            "ph": 6.5,

            "rainfall": 190,

            "soil": "clay",

        }

    }

]

# =====================================================
# Run
# =====================================================

print("=" * 100)
print("MENANAM-AI AGENT TEST")
print("=" * 100)

for i, test in enumerate(tests, start=1):

    print()

    print("=" * 100)
    print(f"TEST {i}")
    print("=" * 100)

    question = test["question"]

    kwargs = test["kwargs"]

    print("QUESTION")
    print(question)

    # --------------------------------------
    # Router Result
    # --------------------------------------

    routing = agent.router.route(question)

    print()

    print("ROUTER")

    print(f"Intent     : {routing['intent']}")
    print(f"Method     : {routing['method']}")
    print(f"Confidence : {routing['confidence']}")

    # --------------------------------------
    # Agent
    # --------------------------------------

    result = agent.ask(
        question,
        **kwargs
    )

    print()

    print("TOOL")
    print(result.get("tool"))

    print()

    print("STATUS")
    print(result.get("status"))

    print()

    print("ANSWER")
    print(result.get("answer"))

    if result.get("tool") == "recommendation":

        print()

        print("TOP RECOMMENDATIONS")

        for rec in result["recommendations"]:

            print(
                f"- {rec['crop']} ({rec['confidence']}%)"
            )

print()

print("=" * 100)
print("TEST FINISHED")
print("=" * 100)
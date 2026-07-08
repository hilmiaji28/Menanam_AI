from menanam_ai.tools.recommendation import RecommendationTool

tool = RecommendationTool()

result = tool.run(

    N=90,

    P=42,

    K=43,

    temperature=27,

    humidity=82,

    ph=6.4,

    rainfall=190,

    soil="clay",

)

print("=" * 100)
print("ANSWER")
print("=" * 100)
print(result["answer"])

print()

print("=" * 100)
print("TOP REKOMENDASI")
print("=" * 100)

for i, rec in enumerate(result["recommendations"], start=1):
    print(
        f"{i}. {rec['crop']} ({rec['confidence']:.2f}%)"
    )

print("=" * 100)
print("HASIL LENGKAP")
print("=" * 100)

for k, v in result.items():
    print(k, ":", v)
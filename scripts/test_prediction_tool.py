from menanam_ai.tools.prediction import PredictionTool

tool = PredictionTool()

result = tool.run(

    crop="Padi",

    temperature=27.5,

    temp_max=31.5,

    temp_min=23.4,

    rainfall=180,

    humidity=82,

    wind_speed=2.3,

    solar_radiation=18.2,

    land_area=2.5,

)

print("=" * 100)
print("ANSWER")
print("=" * 100)
print(result["answer"])

print()

print("=" * 100)
print("FULL RESULT")
print("=" * 100)

for k, v in result.items():
    print(f"{k} : {v}")
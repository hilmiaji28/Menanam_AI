import pandas as pd

from app.services.loader import model_loader


class PredictionService:
    FEATURES = [
        "temperature",
        "temp_max",
        "temp_min",
        "rainfall",
        "humidity",
        "wind_speed",
        "solar_radiation",
        "komoditas_Jagung",
        "komoditas_Padi",
        "komoditas_Singkong",
    ]

    def preprocess(self, request: dict) -> pd.DataFrame:
        data = {
            "temperature": request["temperature"],
            "temp_max": request["temp_max"],
            "temp_min": request["temp_min"],
            "rainfall": request["rainfall"],
            "humidity": request["humidity"],
            "wind_speed": request["wind_speed"],
            "solar_radiation": request["solar_radiation"],

            "komoditas_Jagung": 0,
            "komoditas_Padi": 0,
            "komoditas_Singkong": 0,
        }

        komoditas = request["komoditas"].strip().capitalize()

        if komoditas == "Jagung":
            data["komoditas_Jagung"] = 1

        elif komoditas == "Padi":
            data["komoditas_Padi"] = 1

        elif komoditas == "Singkong":
            data["komoditas_Singkong"] = 1

        else:
            raise ValueError(
                f"Komoditas '{komoditas}' tidak didukung."
            )

        return pd.DataFrame([data])[self.FEATURES]

    def predict(self, request: dict):

        model = model_loader.get_model()

        df = self.preprocess(request)

        prediction = model.predict(df)[0]

        return float(prediction)


prediction_service = PredictionService()
"""
=========================================================

Prediction Tool

Yield Prediction Tool

Input
-----
- Crop
- Weather Features
- Land Area (ha)

Output
------
- Productivity Prediction
- Productivity Level
- Interpretation
- Estimated Yield

=========================================================
"""

from pathlib import Path

import joblib
import pandas as pd

from menanam_ai.core.logger import get_logger
from menanam_ai.core.response import ResponseBuilder

# =====================================================
# Model Path
# =====================================================

ROOT_DIR = Path(__file__).resolve().parents[3]

MODEL_PATH = (
    ROOT_DIR
    / "models"
    / "yield_prediction"
    / "yield_prediction_xgb.pkl"
)

# Jika nanti settings.py sudah digunakan,
# cukup ganti menjadi:
#
# from menanam_ai.config.settings import MODEL_DIR
#
# MODEL_PATH = (
#     MODEL_DIR
#     / "yield_prediction"
#     / "yield_prediction_xgb.pkl"
# )


logger = get_logger(__name__)


class PredictionTool:

    """
    Yield Prediction Tool
    """

    # =====================================================
    # Productivity Threshold
    # Berdasarkan Quartile Dataset Training
    # =====================================================

    PRODUCTIVITY_THRESHOLD = {

        "padi": {
            "q1": 55.6950,
            "q2": 59.1000,
            "q3": 63.1425,
        },

        "jagung": {
            "q1": 57.2300,
            "q2": 66.0200,
            "q3": 76.4200,
        },

        "singkong": {
            "q1": 186.7300,
            "q2": 234.7100,
            "q3": 288.0900,
        },

    }

    # =====================================================
    # Init
    # =====================================================

    def __init__(self):

        logger.info("Loading Yield Prediction Model...")

        self.model = joblib.load(MODEL_PATH)

        logger.info("Yield Prediction Model Loaded Successfully")

    # =====================================================
    # One Hot Encoding
    # =====================================================

    def _encode_crop(self, crop: str):

        crop = crop.lower().strip()

        return {

            "komoditas_Jagung":
                1 if crop == "jagung" else 0,

            "komoditas_Padi":
                1 if crop == "padi" else 0,

            "komoditas_Singkong":
                1 if crop == "singkong" else 0,

        }

    # =====================================================
    # Productivity Level
    # =====================================================

    def _productivity_level(
        self,
        crop: str,
        productivity: float,
    ):

        crop = crop.lower().strip()

        threshold = self.PRODUCTIVITY_THRESHOLD.get(crop)

        if threshold is None:

            return "Tidak diketahui"

        if productivity < threshold["q1"]:

            return "Rendah"

        elif productivity < threshold["q2"]:

            return "Sedang"

        elif productivity < threshold["q3"]:

            return "Tinggi"

        else:

            return "Sangat Tinggi"

    # =====================================================
    # Productivity Interpretation
    # =====================================================

    def _productivity_interpretation(
        self,
        level: str,
    ):

        interpretations = {

            "Sangat Tinggi":
                (
                    "Produktivitas diperkirakan jauh di atas "
                    "rata-rata historis untuk komoditas ini. "
                    "Kondisi cuaca yang diberikan sangat "
                    "mendukung pertumbuhan tanaman."
                ),

            "Tinggi":
                (
                    "Produktivitas diperkirakan berada di atas "
                    "rata-rata historis. Praktik budidaya yang "
                    "baik tetap diperlukan agar potensi hasil "
                    "dapat tercapai."
                ),

            "Sedang":
                (
                    "Produktivitas berada pada kisaran rata-rata "
                    "historis. Pengelolaan pemupukan, irigasi, "
                    "serta pengendalian organisme pengganggu "
                    "tanaman dapat membantu meningkatkan hasil."
                ),

            "Rendah":
                (
                    "Produktivitas diperkirakan berada di bawah "
                    "rata-rata historis. Disarankan melakukan "
                    "evaluasi terhadap kondisi lahan, pemupukan, "
                    "ketersediaan air, serta pengelolaan tanaman."
                ),

            "Tidak diketahui":
                (
                    "Kategori produktivitas tidak dapat "
                    "ditentukan."
                )

        }

        return interpretations.get(
            level,
            "Interpretasi tidak tersedia."
        )

    # =====================================================
    # Prediction
    # =====================================================

    def run(
        self,
        crop: str,
        temperature: float,
        temp_max: float,
        temp_min: float,
        rainfall: float,
        humidity: float,
        wind_speed: float,
        solar_radiation: float,
        land_area: float = 1.0,
    ):

        logger.info(
            f"Prediction Tool | Crop={crop} | Area={land_area} ha"
        )

        try:

            # --------------------------------------------
            # Encode Crop
            # --------------------------------------------

            crop_feature = self._encode_crop(crop)

            # --------------------------------------------
            # DataFrame
            # --------------------------------------------

            df = pd.DataFrame(
                [
                    {
                        "temperature": temperature,
                        "temp_max": temp_max,
                        "temp_min": temp_min,
                        "rainfall": rainfall,
                        "humidity": humidity,
                        "wind_speed": wind_speed,
                        "solar_radiation": solar_radiation,
                        **crop_feature,
                    }
                ]
            )

            # --------------------------------------------
            # Predict
            # --------------------------------------------

            productivity = float(
                self.model.predict(df)[0]
            )

            logger.info(
                f"Prediction={productivity:.2f} kuintal/ha"
            )

            # --------------------------------------------
            # Productivity Level
            # --------------------------------------------

            level = self._productivity_level(
                crop,
                productivity,
            )

            interpretation = (
                self._productivity_interpretation(level)
            )

            # --------------------------------------------
            # Estimated Yield
            # --------------------------------------------

            total_quintal = productivity * land_area

            total_ton = total_quintal / 10

            # --------------------------------------------
            # Natural Language Answer
            # --------------------------------------------

            answer = (

                f"Estimasi produktivitas tanaman "
                f"{crop.title()} adalah "
                f"{productivity:.2f} kuintal/ha.\n\n"

                f"Kategori produktivitas: {level}.\n\n"

                f"Interpretasi:\n"
                f"{interpretation}\n\n"

                f"Dengan luas lahan "
                f"{land_area:.2f} hektar, "

                f"estimasi hasil panen sekitar "
                f"{total_quintal:.2f} kuintal "
                f"({total_ton:.2f} ton)."

            )

            logger.info(
                "Prediction Tool Finished Successfully"
            )

            # --------------------------------------------
            # Success Response
            # --------------------------------------------

            return ResponseBuilder.success(

                tool="prediction",

                intent="prediction",

                answer=answer,

                crop=crop.title(),

                productivity=round(
                    productivity,
                    2,
                ),

                level=level,

                interpretation=interpretation,

                unit="kuintal/ha",

                land_area=land_area,

                estimated_yield_quintal=round(
                    total_quintal,
                    2,
                ),

                estimated_yield_ton=round(
                    total_ton,
                    2,
                ),

            )

        # =================================================
        # Error Handling
        # =================================================

        except Exception as e:

            logger.error(
                f"Prediction Tool Error : {e}"
            )

            return ResponseBuilder.error(

                tool="prediction",

                intent="prediction",

                answer=(
                    "Model prediksi gagal dijalankan."
                ),

                error=str(e),

            )
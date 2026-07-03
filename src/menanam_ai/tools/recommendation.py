"""
=========================================================

Recommendation Tool

Crop Recommendation Tool

Input
-----
- N
- P
- K
- Temperature
- Humidity
- pH
- Rainfall
- Soil Type

Output
------
- Top Crop Recommendation
- Top-3 Recommendation
- Confidence Score
- Recommendation Level

=========================================================
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from menanam_ai.core.logger import get_logger
from menanam_ai.core.response import ResponseBuilder

# =====================================================
# Model Path
# =====================================================

ROOT_DIR = Path(__file__).resolve().parents[3]

MODEL_DIR = (
    ROOT_DIR
    / "models"
    / "crop_recommendation"
)

MODEL_PATH = MODEL_DIR / "crop_recommendation_rf.pkl"

FEATURE_PATH = MODEL_DIR / "crop_recommendation_features.pkl"

LABEL_PATH = MODEL_DIR / "crop_labels.pkl"


# Jika nanti menggunakan settings.py
#
# from menanam_ai.config.settings import MODEL_DIR
#
# MODEL_PATH = MODEL_DIR / "crop_recommendation_rf.pkl"
# FEATURE_PATH = MODEL_DIR / "crop_recommendation_features.pkl"
# LABEL_PATH = MODEL_DIR / "crop_labels.pkl"


logger = get_logger(__name__)


class RecommendationTool:

    """
    Crop Recommendation Tool
    """

    # =====================================================
    # Crop Mapping
    # =====================================================

    CROP_NAME = {

        "rice": "Padi",

        "maize": "Jagung",

        "cassava": "Singkong",

    }

    # =====================================================
    # Init
    # =====================================================

    def __init__(self):

        logger.info("Loading Crop Recommendation Model...")

        self.model = joblib.load(MODEL_PATH)

        self.features = joblib.load(FEATURE_PATH)

        self.labels = joblib.load(LABEL_PATH)

        logger.info("Crop Recommendation Model Loaded Successfully")

    # =====================================================
    # Soil Encoding
    # =====================================================

    def _encode_soil(self, soil: str):

        soil = soil.lower().strip()

        return {

            "soil_clay":
                1 if soil == "clay" else 0,

            "soil_sandy loam":
                1 if soil == "sandy loam" else 0,

            "soil_unknown":
                1 if soil == "unknown" else 0,

        }

    # =====================================================
    # Confidence Level
    # =====================================================

    def _confidence_level(self, confidence: float):

        if confidence >= 90:

            return "Sangat Direkomendasikan"

        elif confidence >= 80:

            return "Direkomendasikan"

        elif confidence >= 60:

            return "Cukup Direkomendasikan"

        else:

            return "Perlu Pertimbangan"

    # =====================================================
    # Recommendation Interpretation
    # =====================================================

    def _interpretation(self, level: str):

        mapping = {

            "Sangat Direkomendasikan":
                (
                    "Model menunjukkan bahwa tanaman ini memiliki "
                    "peluang paling tinggi untuk tumbuh dengan baik "
                    "berdasarkan kondisi tanah dan cuaca yang diberikan."
                ),

            "Direkomendasikan":
                (
                    "Tanaman diperkirakan sesuai dengan kondisi "
                    "lingkungan dan berpotensi memberikan hasil yang baik."
                ),

            "Cukup Direkomendasikan":
                (
                    "Tanaman masih dapat dibudidayakan, namun "
                    "beberapa kondisi lingkungan belum optimal."
                ),

            "Perlu Pertimbangan":
                (
                    "Tingkat keyakinan model relatif rendah. "
                    "Disarankan mengevaluasi kembali kondisi tanah "
                    "dan parameter lingkungan sebelum melakukan penanaman."
                ),

        }

        return mapping.get(

            level,

            "Interpretasi tidak tersedia."

        )
    # =====================================================
    # Recommendation
    # =====================================================

    def run(
        self,
        N: float,
        P: float,
        K: float,
        temperature: float,
        humidity: float,
        ph: float,
        rainfall: float,
        soil: str = "unknown",
    ):

        logger.info(
            f"Recommendation Tool | Soil={soil}"
        )

        try:

            # --------------------------------------------
            # Soil Encoding
            # --------------------------------------------

            soil_feature = self._encode_soil(soil)

            # --------------------------------------------
            # Input Data
            # --------------------------------------------

            row = {

                "N": N,

                "P": P,

                "K": K,

                "temperature": temperature,

                "humidity": humidity,

                "ph": ph,

                "rainfall": rainfall,

                **soil_feature,

            }

            df = pd.DataFrame([row])

            df = df.reindex(

                columns=self.features,

                fill_value=0,

            )

            # --------------------------------------------
            # Predict Probability
            # --------------------------------------------

            probabilities = self.model.predict_proba(df)[0]

            order = np.argsort(probabilities)[::-1]

            recommendations = []

            seen = set()

            for idx in order:

                crop_code = self.model.classes_[idx]

                crop_name = self.CROP_NAME.get(
                    crop_code,
                    crop_code,
                )

                confidence = round(
                    float(probabilities[idx] * 100),
                    2,
                )

                # Skip confidence 0%

                if confidence <= 0:
                    continue

                # Skip duplicate crop

                if crop_name in seen:
                    continue

                seen.add(crop_name)

                recommendations.append(

                    {

                        "crop": crop_name,

                        "confidence": confidence,

                    }

                )

                if len(recommendations) >= 3:
                    break

            # --------------------------------------------
            # No Recommendation
            # --------------------------------------------

            if len(recommendations) == 0:

                return ResponseBuilder.error(

                    tool="recommendation",

                    intent="recommendation",

                    answer=(
                        "Tidak ada rekomendasi tanaman "
                        "yang dapat diberikan."
                    ),

                    error="No recommendation",

                    recommendations=[],

                )

            # --------------------------------------------
            # Best Recommendation
            # --------------------------------------------

            best = recommendations[0]

            level = self._confidence_level(

                best["confidence"]

            )

            interpretation = self._interpretation(

                level

            )

            logger.info(

                f"Best Recommendation = "

                f"{best['crop']} "

                f"({best['confidence']:.2f}%)"

            )

            # --------------------------------------------
            # Build Answer
            # --------------------------------------------

            answer = (

                f"Tanaman yang paling direkomendasikan "

                f"adalah {best['crop']} "

                f"dengan tingkat keyakinan "

                f"{best['confidence']:.2f}%.\n\n"

                f"Kategori rekomendasi: "

                f"{level}.\n\n"

                f"Interpretasi:\n"

                f"{interpretation}"

            )

            # Tambahkan Top Recommendation

            if len(recommendations) > 1:

                answer += "\n\nTOP RECOMMENDATIONS\n"

                for i, item in enumerate(

                    recommendations,

                    start=1,

                ):

                    answer += (

                        f"- {item['crop']} "

                        f"({item['confidence']:.2f}%)\n"

                    )

            logger.info(

                "Recommendation Tool Finished Successfully"

            )

            # --------------------------------------------
            # Success Response
            # --------------------------------------------

            return ResponseBuilder.success(

                tool="recommendation",

                intent="recommendation",

                answer=answer,

                best_crop=best["crop"],

                confidence=best["confidence"],

                level=level,

                interpretation=interpretation,

                recommendations=recommendations,

            )

        # =================================================
        # Error Handling
        # =================================================

        except Exception as e:

            logger.error(

                f"Recommendation Tool Error : {e}"

            )

            return ResponseBuilder.error(

                tool="recommendation",

                intent="recommendation",

                answer=(
                    "Model rekomendasi gagal dijalankan."
                ),

                error=str(e),

                best_crop=None,

                confidence=None,

                level=None,

                interpretation=None,

                recommendations=[],

            )
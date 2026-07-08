"""
=========================================================

Router

Flow

Question
    │
    ▼
Rule Based Router
    │
    ├── Budidaya
    ├── Penyakit
    ├── Prediction
    ├── Recommendation
    │
    └── No Match
            │
            ▼
        LLM Router
            │
            ▼
        Final Intent

=========================================================
"""

from menanam_ai.router.prompt import SYSTEM_PROMPT

from menanam_ai.core.logger import get_logger


logger = get_logger(__name__)


class Router:

    """
    Router untuk menentukan intent pengguna.

    Prioritas:
        1. Rule-based Router
        2. LLM Router (fallback)
    """

    # =====================================================
    # Init
    # =====================================================

    def __init__(self, llm):

        self.llm = llm

        logger.info("Router Initialized")

        # ---------------------------------------------
        # Budidaya Keywords
        # ---------------------------------------------

        self.budidaya = [

            "budidaya",

            "tanam",

            "menanam",

            "pemupukan",

            "pupuk",

            "pengairan",

            "irigasi",

            "panen",

            "benih",

            "bibit",

            "jarak tanam",

            "olah lahan",

            "pengolahan lahan",

            "lahan",

            "penyiangan",

            "penyulaman",

            "gulma",

        ]

        # ---------------------------------------------
        # Disease Keywords
        # ---------------------------------------------

        self.penyakit = [

            "penyakit",

            "hama",

            "blast",

            "bulai",

            "hawar",

            "virus",

            "jamur",

            "bakteri",

            "bercak",

            "busuk",

            "layu",

            "menguning",

            "fungisida",

            "insektisida",

            "pestisida",

            "opt",

        ]

        # ---------------------------------------------
        # Prediction Keywords
        # ---------------------------------------------

        self.prediction = [

            "prediksi",

            "estimasi",

            "hasil panen",

            "produktivitas",

            "yield",

        ]

        # ---------------------------------------------
        # Recommendation Keywords
        # ---------------------------------------------

        self.recommendation = [

            "rekomendasi",

            "cocok",

            "crop recommendation",

            "tanaman apa",

            "tanaman terbaik",

        ]

    # =====================================================
    # Rule Based Router
    # =====================================================

    def _rule_router(self, question: str):

        q = question.lower().strip()

        # ---------------------------------------------
        # Disease
        # ---------------------------------------------

        if any(word in q for word in self.penyakit):

            logger.info(
                "Rule Router -> penyakit"
            )

            return {

                "intent": "penyakit",

                "method": "rule",

                "confidence": 1.0,

            }

        # ---------------------------------------------
        # Prediction
        # ---------------------------------------------

        if any(word in q for word in self.prediction):

            logger.info(
                "Rule Router -> prediction"
            )

            return {

                "intent": "prediction",

                "method": "rule",

                "confidence": 1.0,

            }

        # ---------------------------------------------
        # Recommendation
        # ---------------------------------------------

        if any(word in q for word in self.recommendation):

            logger.info(
                "Rule Router -> recommendation"
            )

            return {

                "intent": "recommendation",

                "method": "rule",

                "confidence": 1.0,

            }

        # ---------------------------------------------
        # Budidaya
        # ---------------------------------------------

        if any(word in q for word in self.budidaya):

            logger.info(
                "Rule Router -> budidaya"
            )

            return {

                "intent": "budidaya",

                "method": "rule",

                "confidence": 1.0,

            }

        logger.info(
            "Rule Router -> No Match"
        )

        return None

    # =====================================================
    # Parse LLM Intent
    # =====================================================

    def _parse_intent(self, response: str) -> str:
        """
        Membersihkan output LLM agar menjadi intent yang valid.
        """

        if not response:
            return "unknown"

        text = (
            response.lower()
            .strip()
            .replace(".", "")
            .replace(",", "")
            .replace(":", "")
            .replace("-", " ")
        )

        valid_intents = [
            "budidaya",
            "penyakit",
            "prediction",
            "recommendation",
            "unknown",
        ]

        for intent in valid_intents:

            if intent in text:

                return intent

        return "unknown"

    # =====================================================
    # LLM Router
    # =====================================================

    def _llm_router(self, question: str):

        logger.info("Fallback -> LLM Router")

        prompt = f"""
{SYSTEM_PROMPT}

Pertanyaan:

{question}
"""

        try:

            response = self.llm.invoke(prompt)

            intent = self._parse_intent(
                response.content
            )

            logger.info(
                f"LLM Router -> {intent}"
            )

            return {

                "intent": intent,

                "method": "llm",

                "confidence": 0.80,

            }

        except Exception as e:

            logger.error(
                f"LLM Router Error : {e}"
            )

            return {

                "intent": "unknown",

                "method": "llm",

                "confidence": 0.0,

            }

    # =====================================================
    # Public API
    # =====================================================

    def route(self, question: str):

        logger.info(
            f"Routing Question : {question}"
        )

        # ---------------------------------------------
        # Rule Router
        # ---------------------------------------------

        result = self._rule_router(question)

        if result is not None:

            logger.info(
                f"Final Intent : "
                f"{result['intent']} "
                f"({result['method']})"
            )

            return result

        # ---------------------------------------------
        # LLM Router
        # ---------------------------------------------

        result = self._llm_router(question)

        logger.info(
            f"Final Intent : "
            f"{result['intent']} "
            f"({result['method']})"
        )

        return result
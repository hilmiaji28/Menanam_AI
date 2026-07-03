"""
=========================================================

Menanam-AI Agent

Single Entry Point

Flow

Question
    │
    ▼
Router
    │
    ├── Budidaya
    │      ▼
    │    RagTool
    │
    ├── Penyakit
    │      ▼
    │   DiseaseTool
    │
    ├── Prediction
    │      ▼
    │ PredictionTool
    │
    ├── Recommendation
    │      ▼
    │ RecommendationTool
    │
    └── Unknown
           ▼
      Default Response

=========================================================
"""

from menanam_ai.router.router import Router

from menanam_ai.tools.rag import RagTool
from menanam_ai.tools.disease import DiseaseTool
from menanam_ai.tools.prediction import PredictionTool
from menanam_ai.tools.recommendation import RecommendationTool

from menanam_ai.core.logger import get_logger
from menanam_ai.core.response import ResponseBuilder


logger = get_logger(__name__)


class Agent:

    """
    Main Agent

    Seluruh request pengguna akan masuk
    melalui class ini kemudian diarahkan
    ke tool yang sesuai menggunakan Router.
    """

    # =====================================================
    # Init
    # =====================================================

    def __init__(self, llm):

        logger.info("Initializing Menanam-AI Agent...")

        # ---------------------------------------------
        # Router
        # ---------------------------------------------

        self.router = Router(llm)

        # ---------------------------------------------
        # Tools
        # ---------------------------------------------

        self.rag_tool = RagTool(llm)

        self.disease_tool = DiseaseTool(llm)

        self.prediction_tool = PredictionTool()

        self.recommendation_tool = RecommendationTool()

        logger.info(
            "Menanam-AI Agent Initialized Successfully"
        )
    # =====================================================
    # Ask
    # =====================================================

    def ask(self, question: str, **kwargs):

        logger.info(f"Agent | Question: {question}")

        try:

            # ---------------------------------------------
            # Router
            # ---------------------------------------------

            routing = self.router.route(question)

            intent = routing.get("intent", "unknown")

            logger.info(
                f"Router -> {intent} "
                f"({routing.get('method', '-')})"
            )

            # ---------------------------------------------
            # Budidaya
            # ---------------------------------------------

            if intent == "budidaya":

                logger.info("Using RagTool")

                result = self.rag_tool.run(question)

                logger.info("RagTool Finished")

                return result

            # ---------------------------------------------
            # Penyakit
            # ---------------------------------------------

            elif intent == "penyakit":

                logger.info("Using DiseaseTool")

                result = self.disease_tool.run(question)

                logger.info("DiseaseTool Finished")

                return result

            # ---------------------------------------------
            # Prediction
            # ---------------------------------------------

            elif intent == "prediction":

                logger.info("Using PredictionTool")

                result = self.prediction_tool.run(**kwargs)

                logger.info("PredictionTool Finished")

                return result

            # ---------------------------------------------
            # Recommendation
            # ---------------------------------------------

            elif intent == "recommendation":

                logger.info("Using RecommendationTool")

                result = self.recommendation_tool.run(**kwargs)

                logger.info("RecommendationTool Finished")

                return result

            # ---------------------------------------------
            # Unknown
            # ---------------------------------------------

            logger.warning(
                f"Unknown Intent : {intent}"
            )

            return ResponseBuilder.error(

                tool="agent",

                intent="unknown",

                answer=(
                    "Maaf, saya belum memahami pertanyaan tersebut.\n\n"
                    "Saya dapat membantu mengenai:\n"
                    "• Budidaya tanaman\n"
                    "• Penyakit tanaman\n"
                    "• Prediksi hasil panen\n"
                    "• Rekomendasi tanaman"
                ),

                error="Unknown intent",

            )

        # =================================================
        # Global Error Handling
        # =================================================

        except Exception as e:

            logger.exception(
                f"Agent Error : {e}"
            )

            return ResponseBuilder.error(

                tool="agent",

                intent="unknown",

                answer=(
                    "Terjadi kesalahan saat memproses permintaan Anda."
                ),

                error=str(e),

            )
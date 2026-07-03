from app.evaluation.dataset import EVALUATION_DATA
from app.evaluation.metrics import EvaluationMetrics

from app.services.loader import model_loader
from app.services.rag_service import rag_service


class RAGEvaluator:

    def initialize(self):

        print("=" * 80)
        print("Loading Resources")
        print("=" * 80)

        model_loader.load_model()
        model_loader.load_embedding()
        model_loader.load_vector_db()
        model_loader.load_retriever()

        print("Resources Ready")
        print("=" * 80)

    def run(self):

        self.initialize()

        metrics = EvaluationMetrics()

        print("=" * 80)
        print("RAG Evaluation")
        print("=" * 80)

        for sample in EVALUATION_DATA:

            result = rag_service.generate_answer(
                sample["question"]
            )

            predicted = result["source_type"]

            expected = sample["expected_source"]

            metrics.update(
                expected,
                predicted,
            )

            print()
            print("Question :", sample["question"])
            print("Expected :", expected)
            print("Predicted:", predicted)
            print("Similarity:", result["similarity_score"])
            print("Confidence:", result["confidence"])
            print("-" * 80)

        print()
        print("=" * 80)
        print(f"Accuracy : {metrics.accuracy():.2%}")
        print("=" * 80)
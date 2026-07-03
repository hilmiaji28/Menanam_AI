from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

# ==========================================================
# BASE DIRECTORY
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

# ==========================================================
# MODEL
# ==========================================================

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "yield_prediction"
    / "yield_prediction_xgb.pkl"
)

# ==========================================================
# VECTOR DATABASE
# ==========================================================

VECTOR_DB_PATH = (
    BASE_DIR
    / "vector_db"
    / "chroma"
)

# ==========================================================
# EMBEDDING
# ==========================================================

EMBEDDING_MODEL = "intfloat/multilingual-e5-base"

DEVICE = "cpu"

# ==========================================================
# GOOGLE GEMINI
# ==========================================================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

GEMINI_MODEL = "gemini-2.5-flash"

TEMPERATURE = 0.2

# ==========================================================
# TAVILY
# ==========================================================

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

MAX_SEARCH_RESULTS = 3

# ==========================================================
# RETRIEVAL
# ==========================================================

TOP_K = 3

FETCH_K = 10

SIMILARITY_THRESHOLD = 0.28

TOP_SCORE_MARGIN = 0.05

MAX_CONTEXT_LENGTH = 3500

MAX_HISTORY = 10

# ==========================================================
# CONFIDENCE
# ==========================================================

ENABLE_CONFIDENCE = True

# ==========================================================
# DEBUG
# ==========================================================

DEBUG = True
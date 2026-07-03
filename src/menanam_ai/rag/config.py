from pathlib import Path

# Root Project
BASE_DIR = Path(__file__).resolve().parents[3]

# Folder
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
VECTOR_DB_DIR = BASE_DIR / "vector_db" / "chroma"

# Embedding
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Chunk
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# Retrieval
TOP_K = 5
SIMILARITY_THRESHOLD = 0.35



import os

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = "gemini-2.5-flash"
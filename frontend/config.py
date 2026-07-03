import os

from pathlib import Path

FASTAPI_URL = os.getenv(
    "FASTAPI_URL",
    "http://127.0.0.1:8000"
)

APP_NAME = "Menanam AI"

PRIMARY_COLOR = "#2E7D32"

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR.parent / "data" / "primary"

STYLE_PATH = BASE_DIR / "style.css"
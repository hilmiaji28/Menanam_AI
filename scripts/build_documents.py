"""
=========================================================

Step 2

Build LangChain Documents

Input:
knowledge_base_raw/

Output:
process/documents.pkl

=========================================================
"""

from pathlib import Path
import pickle
import re
import logging

from langchain_core.documents import Document
import yaml

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

ROOT_DIR = Path(__file__).resolve().parents[1]

KB_DIR = ROOT_DIR / "knowledge_base_raw" / "budidaya"

OUTPUT_DIR = ROOT_DIR / "process"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "documents.pkl"


# ---------------------------------------------------------
# Cleaning
# ---------------------------------------------------------

def clean_markdown(text: str):
    """
    Clean extracted markdown for RAG indexing.

    This function removes formatting noise while preserving
    all meaningful agricultural content.
    """

    # =====================================================
    # Remove YAML Front Matter
    # =====================================================

    text = re.sub(
        r"^---.*?---",
        "",
        text,
        flags=re.DOTALL,
    )

    # =====================================================
    # Remove HTML Page Marker
    # =====================================================

    text = re.sub(
        r"<!--\s*PAGE:.*?-->",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # =====================================================
    # Remove ISBN
    # =====================================================

    text = re.sub(
        r"ISBN[\s0-9\-Xx:]*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # =====================================================
    # Remove URLs
    # =====================================================

    text = re.sub(
        r"https?://\S+",
        "",
        text,
    )

    text = re.sub(
        r"www\.\S+",
        "",
        text,
    )

    # =====================================================
    # Remove Email Address
    # =====================================================

    text = re.sub(
        r"\b[\w\.-]+@[\w\.-]+\.\w+\b",
        "",
        text,
    )

    # =====================================================
    # Remove Copyright Symbols
    # =====================================================

    text = re.sub(
        r"©",
        "",
        text,
    )

    # =====================================================
    # Remove Repeated Footer (Padi Book)
    # =====================================================

    text = re.sub(
        r'Buku Saku untuk Petani Sehat\s*"Ayo Bertani Padi Sehat"',
        "",
        text,
        flags=re.IGNORECASE,
    )

    # =====================================================
    # Remove "BUKU INI TIDAK UNTUK DIPERJUALBELIKAN"
    # =====================================================

    text = re.sub(
        r"BUKU INI TIDAK UNTUK DIPERJUALBELIKAN",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # =====================================================
    # Remove Standalone Page Numbers
    # =====================================================

    text = re.sub(
        r"^\s*\d+\s*$",
        "",
        text,
        flags=re.MULTILINE,
    )

    # =====================================================
    # Remove Long Dot Leaders
    # =====================================================

    text = re.sub(
        r"\.{5,}",
        "",
        text,
    )

    # =====================================================
    # Normalize Spaces
    # =====================================================

    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    # =====================================================
    # Normalize Blank Lines
    # =====================================================

    text = re.sub(
        r"\n\s*\n\s*\n+",
        "\n\n",
        text,
    )

    # =====================================================
    # Strip Leading / Trailing Spaces
    # =====================================================

    return text.strip()


# ---------------------------------------------------------
# Parse metadata
# ---------------------------------------------------------

documents = []

for md in sorted(KB_DIR.rglob("*.md")):

    raw = md.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    m = re.search(
        r"^---(.*?)---",
        raw,
        flags=re.DOTALL
    )

    metadata = yaml.safe_load(m.group(1)) if m else {}

    filename = md.stem.lower()

    if "padi" in filename:
        crop = "padi"
    elif "jagung" in filename:
        crop = "jagung"
    elif "singkong" in filename:
        crop = "singkong"
    else:
        crop = "general"

    metadata = {
        "source": metadata.get("source", md.name),
        "category": metadata.get("category", "budidaya"),
        "crop": crop,
    }

    text = clean_markdown(raw)

    documents.append(
        Document(
            page_content=text,
            metadata=metadata,
        )
    )

logging.info(f"Loaded {len(documents)} documents")

with open(OUTPUT_FILE, "wb") as f:

    pickle.dump(documents, f)

logging.info("documents.pkl created successfully")
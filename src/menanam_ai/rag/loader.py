"""
=========================================================

Load LangChain Documents

Input :
process/documents.pkl

Output :
List[Document]

=========================================================
"""

from pathlib import Path
import pickle
import logging

from langchain_core.documents import Document

# ==========================================================
# FIND PROJECT ROOT
# ==========================================================

CURRENT_FILE = Path(__file__).resolve()

ROOT_DIR = CURRENT_FILE

while not (ROOT_DIR / "pyproject.toml").exists():

    if ROOT_DIR.parent == ROOT_DIR:
        raise RuntimeError(
            "Project root tidak ditemukan."
        )

    ROOT_DIR = ROOT_DIR.parent

# ==========================================================
# CONFIGURATION
# ==========================================================

DOCUMENT_FILE = ROOT_DIR / "process" / "documents.pkl"

# ==========================================================
# LOGGING
# ==========================================================

logger = logging.getLogger(__name__)

# ==========================================================
# LOAD DOCUMENTS
# ==========================================================

def load_documents() -> list[Document]:
    """
    Load LangChain Documents dari process/documents.pkl.

    Returns
    -------
    list[Document]
        List of LangChain Document.
    """

    if not DOCUMENT_FILE.exists():

        raise FileNotFoundError(
            "\n"
            "Document file tidak ditemukan.\n\n"
            f"Expected:\n{DOCUMENT_FILE}\n\n"
            "Silakan jalankan pipeline berikut terlebih dahulu:\n"
            "1. 01_extract_pdf.py\n"
            "2. 02_clean_markdown.py\n"
            "3. 03_semantic_split.py\n"
            "4. 04_build_documents.py\n"
        )

    logger.info("=" * 60)
    logger.info("Loading LangChain Documents")
    logger.info(f"File : {DOCUMENT_FILE}")

    with open(
        DOCUMENT_FILE,
        "rb"
    ) as f:

        documents = pickle.load(f)

    logger.info(f"Loaded : {len(documents)} Documents")
    logger.info("=" * 60)

    if documents:

        logger.info(
            f"First Title : {documents[0].metadata.get('title')}"
        )

    return documents


# ==========================================================
# MAIN (Testing)
# ==========================================================

def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    docs = load_documents()

    print("=" * 60)
    print(f"Total Documents : {len(docs)}")
    print("=" * 60)

    if docs:

        print()

        for i, doc in enumerate(docs[:3], start=1):

            print("=" * 60)

            print(f"Document {i}")

            print("-" * 60)

            print("Metadata")

            print(doc.metadata)

            print()

            print("Content Preview")

            print(doc.page_content[:300])

            print()

if __name__ == "__main__":

    main()
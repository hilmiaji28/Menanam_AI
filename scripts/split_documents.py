from pathlib import Path
import pickle
import logging

from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain_core.documents import Document

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

INPUT_FILE = Path("process/documents.pkl")
OUTPUT_FILE = Path("process/chunks.pkl")

with open(INPUT_FILE, "rb") as f:
    documents = pickle.load(f)

# -----------------------------
# Header Splitter
# -----------------------------

headers_to_split_on = [
    ("#", "header1"),
    ("##", "header2"),
    ("###", "header3"),
]

header_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on,
    strip_headers=False,
)

# -----------------------------
# Character Splitter
# -----------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 700,
    chunk_overlap = 120,
    separators=[
        "\n\n",
        "\n",
        ". ",
        "; ",
        ", ",
        " ",
        "",
    ],
)

chunks = []

for doc in documents:

    # Split berdasarkan markdown header
    md_docs = header_splitter.split_text(doc.page_content)

    for md_doc in md_docs:

        # Gabungkan metadata lama + metadata header
        metadata = {
            **doc.metadata,
            **md_doc.metadata,
        }

        # Split lagi berdasarkan ukuran
        split_docs = text_splitter.split_documents(
            [
                Document(
                    page_content=md_doc.page_content,
                    metadata=metadata,
                )
            ]
        )

        chunks.extend(split_docs)

logging.info(f"Documents : {len(documents)}")
logging.info(f"Chunks    : {len(chunks)}")

with open(OUTPUT_FILE, "wb") as f:
    pickle.dump(chunks, f)

logging.info("chunks.pkl created successfully")
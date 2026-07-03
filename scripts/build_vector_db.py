from pathlib import Path
import pickle
import shutil
import logging

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

INPUT_FILE = Path("process/chunks.pkl")
VECTOR_DB = Path("vector_db/chroma")

EMBEDDING_MODEL = "intfloat/multilingual-e5-base"

with open(INPUT_FILE, "rb") as f:
    chunks = pickle.load(f)

logging.info(f"Loaded {len(chunks)} chunks")

# Prefix "passage:" untuk E5
for chunk in chunks:
    chunk.page_content = f"passage: {chunk.page_content}"

if VECTOR_DB.exists():
    shutil.rmtree(VECTOR_DB)

embedding = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    model_kwargs={
        "device": "cpu"
    },
    encode_kwargs={
        "normalize_embeddings": True
    }
)

vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embedding,
    persist_directory=str(VECTOR_DB)
)

logging.info("Vector DB successfully created")
logging.info(f"Embedding Model : {EMBEDDING_MODEL}")
logging.info(f"Persist Directory : {VECTOR_DB}")
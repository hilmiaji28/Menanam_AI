from pathlib import Path
import pickle

with open("process/documents.pkl", "rb") as f:
    docs = pickle.load(f)

for doc in docs:
    print("=" * 80)
    print(doc.metadata)
    print("Characters :", len(doc.page_content))
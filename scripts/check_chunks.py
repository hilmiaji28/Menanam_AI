import pickle
from statistics import mean

with open("process/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

lengths = [len(c.page_content) for c in chunks]

print(f"Total chunks : {len(chunks)}")
print(f"Min length   : {min(lengths)}")
print(f"Max length   : {max(lengths)}")
print(f"Average      : {mean(lengths):.1f}")

print("\n===== SAMPLE CHUNK =====\n")
print(chunks[0].page_content[:1000])

print("\n===== METADATA =====")
print(chunks[0].metadata)

from collections import Counter

counter = Counter()

for chunk in chunks:
    counter[chunk.metadata["source"]] += 1

print(counter)
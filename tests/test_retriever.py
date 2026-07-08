from menanam_ai.rag.retriever import CropRetriever

retriever = CropRetriever()

questions = [
    "Bagaimana cara pemupukan padi?",
    "Bagaimana syarat tumbuh jagung?",
    "Bagaimana cara pengolahan lahan singkong?",
    "Kapan panen jagung?",
]

for question in questions:

    print("\n")
    print("=" * 100)
    print("QUESTION :", question)
    print("=" * 100)

    docs = retriever.retrieve(question)

    for i, doc in enumerate(docs, start=1):

        print(f"\nTOP {i}")

        print(doc.metadata)

        print()

        print(doc.page_content[:800])
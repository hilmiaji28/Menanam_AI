"""
=========================================================

Step 1

Extract PDF -> Markdown (Budidaya Only)

Input
-----
knowledge_base/budidaya/*.pdf

Output
------
knowledge_base_raw/budidaya/*.md

=========================================================
"""

from pathlib import Path
from docling.document_converter import DocumentConverter

ROOT_DIR = Path(__file__).resolve().parents[1]

INPUT_DIR = ROOT_DIR / "knowledge_base" / "budidaya"
OUTPUT_DIR = ROOT_DIR / "knowledge_base_raw" / "budidaya"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

converter = DocumentConverter()

pdf_files = sorted(INPUT_DIR.glob("*.pdf"))

print("=" * 60)
print(f"Found {len(pdf_files)} Budidaya PDFs")
print("=" * 60)

for pdf in pdf_files:

    print(f"\nProcessing : {pdf.name}")

    result = converter.convert(str(pdf))

    markdown = result.document.export_to_markdown()

    crop = "general"

    name = pdf.stem.lower()

    if "padi" in name:
        crop = "padi"

    elif "jagung" in name:
        crop = "jagung"

    elif "singkong" in name or "ubi" in name:
        crop = "singkong"

    output_file = OUTPUT_DIR / f"{pdf.stem}.md"

    with open(output_file, "w", encoding="utf-8") as f:

        f.write("---\n")
        f.write(f"title: {pdf.stem}\n")
        f.write(f"source: {pdf.name}\n")
        f.write("category: budidaya\n")
        f.write(f"crop: {crop}\n")
        f.write("---\n\n")

        f.write(markdown)

    print(f"Saved : {output_file.relative_to(ROOT_DIR)}")

print("\nExtraction Finished.")
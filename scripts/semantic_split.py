"""
=========================================================

Step 3

Semantic Markdown Splitter

Input :
knowledge_base_clean/

Output :
knowledge_base_semantic/

=========================================================
"""

from aiohttp import client_exceptions
from aiohttp import client_exceptions
from pathlib import Path
import logging
import hashlib
import re
import yaml
import shutil

from slugify import slugify

# ==========================================================
# ROOT DIRECTORY
# ==========================================================

CURRENT_FILE = Path(__file__).resolve()

ROOT_DIR = CURRENT_FILE

while not (ROOT_DIR / "pyproject.toml").exists():

    if ROOT_DIR.parent == ROOT_DIR:
        raise RuntimeError("Project root tidak ditemukan.")

    ROOT_DIR = ROOT_DIR.parent

INPUT_DIR = ROOT_DIR / "knowledge_base_clean"

OUTPUT_DIR = ROOT_DIR / "knowledge_base_semantic"

if OUTPUT_DIR.exists():

    shutil.rmtree(OUTPUT_DIR)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# ==========================================================
# LOGGING
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("SemanticSplitter")

# ==========================================================
# LOAD MARKDOWN FILES
# ==========================================================

md_files = sorted(
    INPUT_DIR.rglob("*.md")
)

logger.info("=" * 60)
logger.info(f"Found {len(md_files)} Markdown Files")
logger.info("=" * 60)

# ==========================================================
# LOAD MARKDOWN
# ==========================================================

def load_markdown(filepath: Path) -> str:
    """
    Load markdown file.
    """

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()


# ==========================================================
# SPLIT FRONT MATTER
# ==========================================================

def split_frontmatter(content: str):
    """
    Memisahkan Front Matter dan Body Markdown.
    """

    if not content.startswith("---"):

        return {}, content

    parts = content.split(
        "---",
        2
    )

    if len(parts) < 3:

        return {}, content

    metadata = yaml.safe_load(parts[1]) or {}

    body = parts[2].strip()

    return metadata, body

# ==========================================================
# IGNORE PAGES
# ==========================================================

IGNORE_KEYWORDS = {

    "KATA PENGANTAR",
    "DAFTAR ISI",
    "TABLE OF CONTENTS",
    "TIM PENYUSUN",
    "PENYUSUN",
    "EDITOR",
    "PENERBIT",
    "ISBN",
    "REFERENSI",
    "DAFTAR PUSTAKA",
    "BIBLIOGRAPHY",
    "LAMPIRAN",
    "UCAPAN TERIMA KASIH",
    "ACKNOWLEDGEMENT",

}


# ==========================================================
# PAGE MARKER
# ==========================================================

PAGE_PATTERN = re.compile(
    r"<!--\s*PAGE:\s*(\d+)\s*-->",
    re.IGNORECASE
)


def extract_page(line: str):

    match = PAGE_PATTERN.match(
        line.strip()
    )

    if match:
        return int(match.group(1))

    return None


# ==========================================================
# MARKDOWN HEADING
# ==========================================================

def markdown_heading_level(line: str):

    line = line.strip()

    if line.startswith("### "):
        return 3

    if line.startswith("## "):
        return 2

    if line.startswith("# "):
        return 1

    return 0


def extract_heading(line: str):

    return line.lstrip("#").strip()


# ==========================================================
# HEADING DETECTION
# ==========================================================

SECTION_KEYWORDS = [

    "Pendahuluan",
    "Syarat Tumbuh",
    "Media Tanam",
    "Iklim",
    "Pemilihan Benih",
    "Varietas",
    "Persemaian",
    "Persiapan Lahan",
    "Pengolahan Lahan",
    "Penanaman",
    "Pengairan",
    "Pemupukan",
    "Penjarangan",
    "Penyiangan",
    "Pembumbunan",
    "Perawatan",
    "Fase Pertumbuhan",
    "Hama",
    "Penyakit",
    "Gejala",
    "Penyebab",
    "Pengendalian",
    "Pencegahan",
    "Panen",
    "Pasca Panen",
    "Standar Mutu"

]


def markdown_heading_level(line):

    line = line.strip()

    if line.startswith("### "):
        return 3

    if line.startswith("## "):
        return 2

    if line.startswith("# "):
        return 1

    return 0


def extract_heading(line):

    return line.lstrip("#").strip()


def normalize_heading(text):

    text = text.replace("#", "")

    text = text.strip()

    text = text.rstrip(":")

    # hilangkan angka
    text = re.sub(
        r"^[0-9]+(\.[0-9]+)*\s*",
        "",
        text
    )

    # hilangkan A.
    text = re.sub(
        r"^[A-Z]\.\s*",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.title()


def detect_section(text):

    text_lower = normalize_heading(text).lower()

    for keyword in SECTION_KEYWORDS:

        if keyword.lower() in text_lower:

            return keyword

    return None

def looks_like_heading(text: str) -> bool:

    text = text.strip()

    if len(text) < 3:
        return False

    if len(text) > 60:
        return False

    if text.endswith("."):
        return False

    if text.endswith(":"):
        return False

    if any(ch.isdigit() for ch in text):
        return False

    alpha = sum(c.isalpha() for c in text)

    if alpha < 3:
        return False

    upper_ratio = sum(c.isupper() for c in text if c.isalpha()) / alpha

    return upper_ratio >= 0.75

# ==========================================================
# CHUNK CONFIG
# ==========================================================

MAX_WORDS = 400

OVERLAP = 50

MIN_WORDS = 40

# ==========================================================
# SECTION TO IGNORE
# ==========================================================

IGNORE_SECTIONS = {

    "kata pengantar",

    "pengantar",

    "foreword",

    "preface",

    "daftar isi",

    "contents",

    "tim penyusun",

    "penyusun",

    "editor",

    "isbn",

    "copyright",

    "hak cipta",

    "ucapan terima kasih",

    "tentang penulis"

}

def should_ignore_section(section: str):

    if not section:

        return False

    section = section.lower().strip()

    return section in IGNORE_SECTIONS

# ==========================================================
# IGNORE CHUNK
# ==========================================================

IGNORE_PATTERNS = [

    "isbn",

    "hak cipta",

    "all rights reserved",

    "dicetak oleh",

    "tim penyusun",

    "editor",

    "kata pengantar",

    "ucapan terima kasih"

]

def should_ignore_chunk(text):

    text_lower = text.lower()

    if len(text.split()) < MIN_WORDS:

        return True

    for pattern in IGNORE_PATTERNS:

        if pattern in text_lower:

            return True

    return False

# ==========================================================
# DETECT CROP
# ==========================================================

def detect_crop(source):

    source = source.lower()

    if "jagung" in source:
        return "jagung"

    if "padi" in source:
        return "padi"

    if "singkong" in source:
        return "singkong"

    if "cassava" in source:
        return "singkong"

    return "unknown"


# ==========================================================
# DETECT CATEGORY
# ==========================================================

def detect_category(source):

    source = source.lower()

    if "budidaya" in source:
        return "budidaya"

    if "penyakit" in source:
        return "penyakit"

    return "unknown"

# ==========================================================
# BUILD METADATA
# ==========================================================

def build_metadata(

    base_metadata,
    title,
    section,
    page

):

    metadata = base_metadata.copy()

    metadata["title"] = title

    metadata["section"] = section

    metadata["page"] = page

    source = metadata.get(
        "source",
        ""
    ) 

    source = metadata.get("source", "")

    metadata["crop"] = detect_crop(source).lower()

    metadata["category"] = detect_category(source).lower()

    metadata.pop(
        "generated",
        None
    )

    return metadata


# ==========================================================
# SPLIT LONG CHUNK
# ==========================================================

def split_long_chunk(text):

    words = text.split()

    if len(words) <= MAX_WORDS:

        return [text]

    chunks = []

    overlap = 50

    step = MAX_WORDS - overlap

    for i in range(

        0,

        len(words),

        step

    ):

        part = words[

            i:i + MAX_WORDS

        ]

        chunks.append(

            " ".join(part)

        )

    return chunks

def is_table_of_contents(text: str):

    lines = text.split("\n")

    count = 0

    for line in lines:

        if re.search(r"Hal\.\s*\d+", line):

            count += 1

    return count >= 5

# ==========================================================
# SEMANTIC SPLITTER
# ==========================================================

def semantic_split(

    body,
    base_metadata

):

    # ------------------------------------
    # Normalisasi title
    # ------------------------------------

    if "title" in base_metadata:

        base_metadata["title"] = (

            base_metadata["title"]

            .replace("_", " ")

            .replace(" ID", "")

            .strip()

        )

    lines = body.split("\n")

    semantic_chunks = []

    buffer = []

    current_page = 1

    current_title = base_metadata.get(
        "title",
        "General"
    )

    current_section = "General"

    # ------------------------------------
    # Save Chunk
    # ------------------------------------

    def save_current_chunk():

        nonlocal buffer

        if not buffer:
            return

        text = "\n".join(buffer).strip()

        buffer = []

        print("=" * 50)
        print("TEXT PREVIEW")
        print(text[:300])
        print("WORDS :", len(text.split()))
        print("=" * 50)

        if is_table_of_contents(text):

            return

        if len(text.split()) < MIN_WORDS:

            return

        if should_ignore_chunk(text):
            return

        for chunk_text in split_long_chunk(text):

            metadata = build_metadata(

                base_metadata,

                current_title,

                current_section,

                current_page

            )

            semantic_chunks.append(

                {

                    "metadata": metadata,

                    "text": chunk_text

                }

            )

    # ------------------------------------
    # Main Loop
    # ------------------------------------

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # PAGE
        page = extract_page(line)

        if page is not None:
            save_current_chunk()
            current_page = page
            continue

        # MARKDOWN
        level = markdown_heading_level(line)

        if level > 0:

            save_current_chunk()

            heading = normalize_heading(
                extract_heading(line)
            )

            if should_ignore_section(heading):
                continue

            if level == 1:
                current_title = heading
                current_section = "General"
            else:
                current_section = heading

            continue

        # PDF SECTION
        detected = detect_section(line)

        if detected:

            save_current_chunk()

            current_section = detected

            continue

        # CONTENT
        buffer.append(line)

    # Setelah loop selesai
    save_current_chunk()

    logger.info(
        f"Semantic Chunks : {len(semantic_chunks)}"
    )

    return semantic_chunks
# ==========================================================
# DUPLICATE HASH
# ==========================================================

def text_hash(text: str):

    return hashlib.md5(
        text.strip().lower().encode("utf-8")
    ).hexdigest()


# ==========================================================
# REMOVE DUPLICATE CHUNKS
# ==========================================================

def remove_duplicate_chunks(chunks):

    unique_chunks = []

    seen = set()

    duplicate = 0

    for chunk in chunks:

        h = text_hash(
            chunk["text"]
        )

        if h in seen:

            duplicate += 1
            continue

        seen.add(h)

        unique_chunks.append(chunk)

    logger.info(
        f"Duplicate Removed : {duplicate}"
    )

    return unique_chunks


# ==========================================================
# FILENAME GENERATOR
# ==========================================================

def create_filename(metadata, text):

    title = slugify(
        metadata["title"],
        separator="_"
    )

    section = slugify(
        metadata["section"],
        separator="_"
    )

    page = metadata["page"]

    short_hash = hashlib.md5(
        text.encode("utf-8")
    ).hexdigest()[:8]

    return (
        f"{title}_{section}_page_{page}_{short_hash}.md"
    )

# ==========================================================
# MARKDOWN WRITER
# ==========================================================

def save_chunks(chunks):

    total_saved = 0

    for chunk in chunks:

        metadata = chunk["metadata"]

        category = metadata["category"]
        crop = metadata["crop"]

        save_dir = (

            OUTPUT_DIR

            / category

            / crop

        )

        save_dir.mkdir(

            parents=True,

            exist_ok=True

        )

        filename = create_filename(
            metadata,
            chunk["text"]
        )

        output_file = save_dir / filename

        yaml_text = yaml.dump(

            metadata,

            allow_unicode=True,

            sort_keys=False

        )

        with open(

            output_file,

            "w",

            encoding="utf-8"

        ) as f:

            f.write("---\n")

            f.write(yaml_text)

            f.write("---\n\n")

            f.write(
                chunk["text"]
            )

        total_saved += 1

    logger.info(
        f"Saved {total_saved} Semantic Chunks"
    )

    return total_saved

# ==========================================================
# MAIN
# ==========================================================

def main():

    logger.info("=" * 60)
    logger.info("Semantic Split Started")
    logger.info("=" * 60)

    total_documents = 0
    total_chunks = 0

    for md in md_files:

        logger.info(f"Processing : {md.name}")

        # ------------------------------------------
        # Load markdown
        # ------------------------------------------

        content = load_markdown(md)

        base_metadata, body = split_frontmatter(
            content
        )

        # ------------------------------------------
        # Semantic Split
        # ------------------------------------------

        chunks = semantic_split(

            body,

            base_metadata

        )

        logger.info(
            f"Generated : {len(chunks)} chunks"
        )

        # ------------------------------------------
        # Remove duplicate
        # ------------------------------------------

        chunks = remove_duplicate_chunks(
            chunks
        )

        # ------------------------------------------
        # Save semantic markdown
        # ------------------------------------------

        saved = save_chunks(
            chunks
        )

        total_documents += 1

        total_chunks += saved

        logger.info("-" * 60)

    logger.info("=" * 60)
    logger.info("Semantic Split Finished")
    logger.info(f"Processed Documents : {total_documents}")
    logger.info(f"Generated Chunks    : {total_chunks}")
    logger.info("=" * 60)
    

# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":

    main()
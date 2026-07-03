from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[2]

STYLE_PATH = BASE_DIR / "frontend" / "style.css"

with open(STYLE_PATH, encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True,
    )

st.set_page_config(
    page_title="Tentang Menanam AI",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Tentang Menanam AI")

st.markdown("""
Menanam AI adalah aplikasi berbasis Artificial Intelligence (AI)
yang membantu petani dan masyarakat Indonesia dalam memperoleh
informasi budidaya tanaman serta memperkirakan produktivitas panen.

Aplikasi ini menggabungkan Machine Learning, Retrieval-Augmented Generation (RAG),
dan Large Language Model (LLM) sehingga mampu memberikan jawaban
yang lebih akurat berdasarkan Knowledge Base maupun Internet Search.
""")

st.divider()

# ======================================================
# FITUR
# ======================================================

st.header("✨ Fitur")

col1, col2 = st.columns(2)

with col1:

    st.success("🌾 Prediksi Produktivitas")

    st.write("""
- Prediksi produktivitas tanaman

- Estimasi hasil panen

- Rekomendasi berdasarkan hasil prediksi
""")

with col2:

    st.success("🤖 AI Assistant")

    st.write("""
- Menjawab pertanyaan pertanian

- Hybrid RAG

- Internet Search Fallback

- Multi-turn Conversation
""")

st.divider()

# ======================================================
# TECH STACK
# ======================================================

st.header("🛠 Tech Stack")

st.markdown("""
### Backend

- FastAPI
- XGBoost
- ChromaDB
- LangChain
- HuggingFace Embedding
- Google Gemini 2.5 Flash
- Tavily Search

### Frontend

- Streamlit

### Machine Learning

- Scikit-Learn
- XGBoost

### Database

- Chroma Vector Database

### Embedding

- intfloat/multilingual-e5-base
""")

st.divider()

# ======================================================
# MODEL
# ======================================================

st.header("🧠 AI Architecture")

st.code("""
User

↓

Streamlit

↓

FastAPI

↓

Prediction API
        │
        ├── XGBoost
        │
        └── Hybrid RAG
                │
                ├── ChromaDB
                ├── Gemini 2.5 Flash
                └── Internet Search
""")

st.divider()

# ======================================================
# DATASET
# ======================================================

st.header("📊 Dataset")

st.markdown("""
Dataset yang digunakan berasal dari:

- NASA POWER
- Data Produktivitas Tanaman Jawa Barat
- Knowledge Base Budidaya Tanaman
- Dokumen Pertanian Indonesia
""")

st.divider()

# ======================================================
# DEVELOPER
# ======================================================

st.header("👨‍💻 Developer")

st.write("Hilmi Aji")

st.write("AI Engineer | Machine Learning | Sales & Business Management")

st.info(
    "Menanam AI dibuat sebagai Final Project Machine Learning & AI Engineering."
)
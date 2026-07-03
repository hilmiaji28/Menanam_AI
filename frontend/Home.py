import streamlit as st

from components.sidebar import sidebar
from services.api import api
from config import DATA_DIR, STYLE_PATH


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Menanam AI",
    page_icon="🌱",
    layout="wide"
)

sidebar()

# =====================================================
# HEADER
# =====================================================

st.title("🌱 Menanam AI")

st.subheader(
    "AI-powered Smart Agriculture Assistant"
)

st.write(
    """
Menanam AI membantu petani memperoleh informasi budidaya tanaman,
memprediksi produktivitas panen,
serta memberikan rekomendasi menggunakan Artificial Intelligence.
"""
)

st.divider()

# =====================================================
# HEALTH STATUS
# =====================================================

st.subheader("📡 System Status")

health = api.health()

if "error" in health:

    st.error(health["error"])

else:

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        if health.get("status") == "healthy":

            st.success("🟢 Backend")

        else:

            st.error("🔴 Backend")

    with col2:

        if health.get("prediction_model"):

            st.success("🌾 Prediction Model")

        else:

            st.error("Prediction Model")

    with col3:

        if health.get("vector_db"):

            st.success("📚 Knowledge Base")

        else:

            st.error("Knowledge Base")

    with col4:

        if health.get("retriever"):

            st.success("🤖 AI Assistant")

        else:

            st.error("Retriever")

st.divider()

# =====================================================
# FEATURES
# =====================================================

st.subheader("🚀 Features")

col1, col2 = st.columns(2)

with col1:

    st.info("🌾 Productivity Prediction")

    st.write(
        """
Prediksi produktivitas tanaman menggunakan
Machine Learning berbasis XGBoost.
"""
    )

    st.success("✔ Productivity Prediction")

    st.success("✔ Yield Estimation")

    st.success("✔ Smart Recommendation")

with col2:

    st.info("🤖 AI Assistant")

    st.write(
        """
Menjawab pertanyaan pertanian menggunakan
Hybrid Retrieval-Augmented Generation.
"""
    )

    st.success("✔ Knowledge Base")

    st.success("✔ Internet Search")

    st.success("✔ Multi-turn Conversation")

st.divider()

# =====================================================
# TECHNOLOGY
# =====================================================

st.subheader("⚙️ Technology")

tech1, tech2, tech3, tech4 = st.columns(4)

with tech1:

    st.metric(
        "Machine Learning",
        "XGBoost"
    )

with tech2:

    st.metric(
        "Embedding",
        "E5-base"
    )

with tech3:

    st.metric(
        "LLM",
        "Gemini 2.5 Flash"
    )

with tech4:

    st.metric(
        "Backend",
        "FastAPI"
    )

st.divider()

# =====================================================
# AI ARCHITECTURE
# =====================================================

st.subheader("🧠 AI Pipeline")

st.code(
"""
User
    │
    ▼
Streamlit
    │
    ▼
FastAPI
    │
    ├──────── Prediction (XGBoost)
    │
    └──────── AI Assistant
                 │
                 ├── ChromaDB
                 ├── Gemini 2.5 Flash
                 ├── Internet Search
                 └── Hybrid RAG
"""
)

st.divider()

# =====================================================
# FOOTER
# =====================================================

st.caption(
    "🌱 Menanam AI • Built with FastAPI, Streamlit, XGBoost, ChromaDB, LangChain, Gemini 2.5 Flash, dan Tavily Search."
)
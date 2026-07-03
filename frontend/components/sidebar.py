import streamlit as st

from services.api import api


def sidebar():

    # =====================================================
    # LOGO
    # =====================================================

    st.sidebar.title("🌱 Menanam AI")

    st.sidebar.caption(
        "Smart Agriculture Assistant"
    )

    st.sidebar.divider()

    # =====================================================
    # BACKEND STATUS
    # =====================================================

    health = api.health()

    if "error" in health:

        st.sidebar.error(
            "🔴 Backend Offline"
        )

        st.sidebar.caption(
            health["error"]
        )

        st.sidebar.divider()

        st.sidebar.warning(
            """
Backend belum dapat dihubungkan.

Pastikan FastAPI sedang berjalan.
"""
        )

        return

    st.sidebar.success(
        "🟢 Backend Online"
    )

    st.sidebar.divider()

    # =====================================================
    # MODEL STATUS
    # =====================================================

    st.sidebar.subheader("Status Sistem")

    if health.get("prediction_model"):

        st.sidebar.success(
            "🌾 Prediction Model"
        )

    else:

        st.sidebar.error(
            "Prediction Model"
        )

    if health.get("embedding"):

        st.sidebar.success(
            "🧠 Embedding"
        )

    else:

        st.sidebar.error(
            "Embedding"
        )

    if health.get("vector_db"):

        st.sidebar.success(
            "📚 Knowledge Base"
        )

    else:

        st.sidebar.error(
            "Knowledge Base"
        )

    if health.get("retriever"):

        st.sidebar.success(
            "🔎 Retriever"
        )

    else:

        st.sidebar.error(
            "Retriever"
        )

    st.sidebar.divider()

    # =====================================================
    # MODEL INFO
    # =====================================================

    st.sidebar.subheader("Teknologi")

    st.sidebar.markdown(
        """
- FastAPI
- Streamlit
- XGBoost
- ChromaDB
- LangChain
- Gemini 2.5 Flash
- Tavily Search
"""
    )

    st.sidebar.divider()

    # =====================================================
    # VERSION
    # =====================================================

    st.sidebar.caption(
        "Menanam AI v1.0"
    )

    st.sidebar.caption(
        "© 2026 Hilmi Aji"
    )
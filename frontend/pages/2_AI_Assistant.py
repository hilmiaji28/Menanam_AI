import streamlit as st

from components.sidebar import sidebar
from services.api import api
from config import DATA_DIR, STYLE_PATH


with open("style.css") as f:

    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )


st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

sidebar()

st.title("🤖 Menanam AI Assistant")

st.caption(
    "Tanyakan apa saja mengenai budidaya tanaman, hama, penyakit, pemupukan, maupun teknik pertanian."
)

# ==========================================================
# SESSION
# ==========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []

if "quick_prompt" not in st.session_state:

    st.session_state.quick_prompt = None


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.divider()

    st.subheader("💬 AI Assistant")

    if st.button(
        "🗑 Hapus Percakapan",
        use_container_width=True
    ):

        st.session_state.messages.clear()

        st.toast(
            "Percakapan berhasil dihapus."
        )

        st.rerun()

    st.divider()

    st.subheader("Contoh Pertanyaan")

    examples = [

        "Bagaimana memilih benih padi?",

        "Bagaimana mengatasi penyakit blas?",

        "Kapan waktu tanam jagung?",

        "Bagaimana pemupukan singkong?"

    ]

    for ex in examples:

        if st.button(
            ex,
            use_container_width=True
        ):

            st.session_state.quick_prompt = ex

            st.rerun()


# ==========================================================
# HISTORY
# ==========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            st.divider()

            if message["source_type"] == "knowledge_base":

                st.success("📚 Knowledge Base")

            else:

                st.info("🌐 Internet")

            col1, col2 = st.columns(2)

            with col1:

                if message["similarity_score"] is not None:

                    st.metric(
                        "Similarity",
                        f"{message['similarity_score']:.3f}"
                    )

            with col2:

                if message["confidence"] is not None:

                    st.metric(
                        "Confidence",
                        f"{message['confidence']:.3f}"
                    )

            if len(message["sources"]) > 0:

                with st.expander("📄 Referensi"):

                    for source in message["sources"]:

                        st.write(f"• {source}")

# ==========================================================
# USER INPUT
# ==========================================================

question = (
    st.session_state.pop("quick_prompt", None)
    or st.chat_input("Ketik pertanyaan Anda...")
)

# ==========================================================
# SEND MESSAGE
# ==========================================================

if question:

    # -------------------------------
    # Tampilkan pesan user
    # -------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    # -------------------------------
    # Build History
    # -------------------------------

    history = []

    # maksimal 10 chat terakhir
    for msg in st.session_state.messages[-10:]:

        history.append(
            {
                "role": msg["role"],
                "content": msg["content"],
            }
        )

    # -------------------------------
    # Assistant
    # -------------------------------

    with st.chat_message("assistant"):

        placeholder = st.empty()

        placeholder.info(
            "🧠 Menanam AI sedang menganalisis pertanyaan..."
        )

        result = api.assistant(
            question=question,
            history=history,
        )

        placeholder.empty()

        # ---------------------------
        # Error
        # ---------------------------

        if "error" in result:

            st.error(result["error"])

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": result["error"],
                    "source_type": "system",
                    "similarity_score": None,
                    "confidence": None,
                    "sources": [],
                }
            )

            st.stop()

        # ---------------------------
        # Answer
        # ---------------------------

        answer = result.get(
            "answer",
            "Tidak ada jawaban."
        )

        st.markdown(answer)

        st.divider()

        source_type = result.get(
            "source_type",
            "knowledge_base"
        )

        if source_type == "knowledge_base":

            st.success("📚 Jawaban berasal dari Knowledge Base")

        else:

            st.info("🌐 Jawaban berasal dari Internet Search")

        similarity = result.get(
            "similarity_score"
        )

        confidence = result.get(
            "confidence"
        )

        col1, col2 = st.columns(2)

        with col1:

            if similarity is not None:

                st.metric(
                    "Similarity",
                    f"{similarity:.3f}"
                )

        with col2:

            if confidence is not None:

                st.metric(
                    "Confidence",
                    f"{confidence:.3f}"
                )

        sources = result.get(
            "sources",
            []
        )

        if len(sources) > 0:

            with st.expander(
                "📄 Referensi"
            ):

                for source in sources:

                    st.write(f"• {source}")

    # -------------------------------
    # Save Assistant Message
    # -------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "source_type": source_type,
            "similarity_score": similarity,
            "confidence": confidence,
            "sources": sources,
        }
    )

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "🌱 Menanam AI • AI Assistant menggunakan Hybrid RAG, Gemini 2.5 Flash, ChromaDB, dan Internet Search."
)
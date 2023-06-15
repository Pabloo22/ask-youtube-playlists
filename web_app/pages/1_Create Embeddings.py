import streamlit as st

from ask_youtube_playlists.data_processing import (EMBEDDING_MODELS_NAMES,
                                                   get_embedding_model,)


st.set_page_config(
    page_title="Extractive QA",
    page_icon="🔍",
)

st.title("Extractive Question Answering")

# ---------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
            <style>
            .sidebar .sidebar-content {
                min-width: 180px;
            }
            </style>
        """, unsafe_allow_html=True)

    st.header("Select Embedding Model")
    embedding_model = st.selectbox("Select Embedding Model",
                                   EMBEDDING_MODELS_NAMES,
                                   key="embedding_model")

    st.header("Set hyperparameters")

    chunk_size = st.slider("Select Chunk Size",
                           min_value=128,
                           max_value=512,
                           value=320,
                           step=1)

    overlap = st.slider("Select Overlap",
                        min_value=0,
                        max_value=128,
                        value=64,
                        step=1)
    # --------------------------------------------------------------------
    st.header()
    # Add a button to process the data
    if st.button("Process Data"):
        pass


embedding_model = get_embedding_model(embedding_model)


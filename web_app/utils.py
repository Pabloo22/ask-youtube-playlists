import pathlib
import streamlit as st


from ask_youtube_playlists.data_processing import (EMBEDDING_MODELS_NAMES,
                                                   get_embedding_model,
                                                   )



def get_data_directory() -> pathlib.Path:
    """Returns the path to the data directory."""
    parent_path = pathlib.Path(__file__).parent
    while parent_path.name != "ask-youtube-playlists":
        parent_path = parent_path.parent

    data_directory = parent_path / "data"
    return data_directory


def get_embedding_model_streamlit():
    st.header("Select Embedding Model")
    embedding_model_name = st.selectbox("Select Embedding Model",
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

    num_docs = st.slider("Select Number of Documents to Retrieve",
                         min_value=1,
                         max_value=10,
                         value=5,
                         step=1)

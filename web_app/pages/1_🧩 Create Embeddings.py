import pathlib
import streamlit as st
import dotenv

from ask_youtube_playlists.data_processing import (EMBEDDING_MODELS_NAMES,
                                                   create_embeddings_pipeline,
                                                   )

st.set_page_config(
    page_title="Create Embeddings",
    page_icon="🧩",
)


dotenv.load_dotenv()

def get_data_directory() -> pathlib.Path:
    """Returns the path to the data directory."""
    parent_path = pathlib.Path(__file__).parent
    while parent_path.name != "ask-youtube-playlists":
        parent_path = parent_path.parent

    data_directory = parent_path / "data"
    return data_directory


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
    embedding_model_name = st.selectbox("Select Embedding Model",
                                        EMBEDDING_MODELS_NAMES)

    st.header("Set hyperparameters")

    chunk_size = st.slider("Select Chunk Size",
                           min_value=128,
                           max_value=1024,
                           value=320,
                           step=1)

    overlap = st.slider("Select Overlap",
                        min_value=0,
                        max_value=128,
                        value=64,
                        step=1)


# --------------------------------------------------------------------


def main():
    if "loaded_playlist_names" not in st.session_state:
        st.session_state["loaded_playlist_names"] = []

    playlist_list = st.session_state["loaded_playlist_names"]

    if playlist_list:
        playlist_name = st.selectbox("Select Loaded Playlist",
                                     playlist_list)

        if st.button("Create Embeddings"):
            embedding_dir_name = f"{embedding_model_name}_" \
                                 f"{chunk_size}_{overlap}"

            data_directory_parent = get_data_directory().parent
            data_directory = data_directory_parent / "data"

            playlist_dir = data_directory / playlist_name  # type: ignore
            retriever_dir = playlist_dir / embedding_dir_name
            create_embeddings_pipeline(retriever_dir,
                                       embedding_model_name,  # type: ignore
                                       max_chunk_size=chunk_size,
                                       min_overlap_size=overlap,
                                       use_st_progress_bar=True)
    else:
        st.error("No playlists loaded. Please load a playlist first.")


if __name__ == "__main__":
    main()

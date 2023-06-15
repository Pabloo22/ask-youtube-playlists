import pathlib
import streamlit as st

import dotenv

from ask_youtube_playlists.data_processing import get_available_directories
from ask_youtube_playlists.question_answering import (
    get_extractive_answer,
    get_generative_answer,
    EXTRACTIVE_MODEL_NAMES,
    GENERATIVE_MODEL_NAMES,
    Retriever,
    load_model,
)

st.set_page_config(
    page_title="Generative QA",
    page_icon="🧠",
)

# Load OPENAI_API_KEY from .env file
dotenv.load_dotenv()


def get_data_directory() -> pathlib.Path:
    """Returns the path to the data directory."""
    parent_path = pathlib.Path(__file__).parent
    while parent_path.name != "ask-youtube-playlists":
        parent_path = parent_path.parent

    data_directory = parent_path / "data"
    return data_directory


data_dir = get_data_directory()
if "playlist_list" not in st.session_state:
    st.session_state["playlist_list"] = get_available_directories(data_dir)


if "selected_playlists" not in st.session_state:
    st.session_state["selected_playlists"] = []

selected_playlists = st.session_state["selected_playlists"]


generative_models = GENERATIVE_MODEL_NAMES
extractive_models = EXTRACTIVE_MODEL_NAMES

playlist_list = st.session_state["loaded_playlist_names"]
if 'mode' not in st.session_state:
    st.session_state['mode'] = 'extractive'

mode = st.session_state['mode']

st.title("Question Answering")

# Sidebar ---------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
            <style>
            .sidebar .sidebar-content {
                min-width: 180px;
            }
            </style>
        """, unsafe_allow_html=True)
    st.header("Set mode")
    mode_radio = st.radio("Select a mode",
                          ['extractive', 'generative'],
                          key="mode_radio")
    if mode_radio != mode:
        st.session_state['mode'] = mode_radio
        st.experimental_rerun()

    st.header("Set model")
    if mode == 'generative':
        generative_model = st.selectbox("Select a Generative Model",
                                        generative_models,
                                        key="generative_model")
    elif mode == 'extractive':
        extractive_model = st.selectbox("Select an Extractive Model",
                                        extractive_models,
                                        key="extractive_model")
    st.header("Set hyperparameters")
    if mode == 'generative':
        # slider to choose temperature
        temperature = st.slider("Select Temperature",
                                min_value=0.0,
                                max_value=1.0,
                                value=0.7,
                                step=0.05)

        max_length = st.slider("Enter max_length value",
                               min_value=10,
                               max_value=8000,
                               value=50,
                               step=10)

    max_retrieved_docs = 100 if mode == "generative" else 10
    n_retrieved_docs = st.slider("Select number of returned documents",
                                 min_value=1,
                                 max_value=max_retrieved_docs,
                                 value=10,
                                 step=1)

# -----------------------------------------------------------------------------

# Initialize 'answer', 'retrievers', 'question' and 'relevant_documents'
# in session state
if 'answer' not in st.session_state:
    st.session_state['answer'] = None
if 'retrievers' not in st.session_state:
    st.session_state['retrievers'] = []
if 'question' not in st.session_state:
    st.session_state['question'] = ""
if 'relevant_documents' not in st.session_state:
    st.session_state['relevant_documents'] = []


# Playlist selection, multiple playlists can be selected
# From st.session_state["playlist_list"] create checkboxes
# for each playlist
retrievers = []
for playlist_name in st.session_state["playlist_list"]:
    checkbox_value = st.checkbox(playlist_name, key=playlist_name)

    if checkbox_value:
        # Select the embeddings model
        data_dir = get_data_directory()
        playlist_directory = data_dir / playlist_name
        embeddings = get_available_directories(playlist_directory)
        embeddings = [embedding for embedding in embeddings
                      if embedding != "raw"]
        selected_retriever = st.radio("Select an Embeddings Model",
                                      embeddings)

        retriever_path = playlist_directory / selected_retriever
        retriever = Retriever(retriever_path)
        retrievers.append(retriever)

if retrievers:
    st.subheader("Ask Question")
    # Receive question input
    question = st.text_input("Enter your question", key="question")

    if question != "":
        question = st.session_state['question']

        # Retrieve relevant documents
        relevant_documents = Retriever.retrieve(retrievers,
                                                question,
                                                n_retrieved_docs)
        st.session_state['relevant_documents'] = relevant_documents

        if mode == 'extractive':
            st.subheader("Extractive Answer")
            for i, document_info in enumerate(relevant_documents, start=1):

                answer = get_extractive_answer(
                    question,
                    document_info.document.page_content,
                    extractive_model,  # type: ignore
                )
                playlist_name = document_info.playlist_name
                # Expand the answer
                with st.expander(f"Answer {i} from {playlist_name}"):
                    st.write(answer)

        if mode == 'generative':
            st.subheader("Generative Answer")
            docs = [document_info.document
                    for document_info in relevant_documents]
            answer = get_generative_answer(
                question,
                relevant_documents=docs,
                model_name=generative_model,  # type: ignore
                temperature=temperature,
                max_length=max_length
            )
            st.write(answer)
            # st.write(relevant_documents)
            # st.write(retrievers)

            # st.subheader("Sources")
            # for i, document_info in enumerate(relevant_documents, start=1):
            #     playlist_name = document_info.playlist_name
            #     # Expand the answer
            #     with st.expander(f"Document {i} from {playlist_name}"):
            #         st.write(answer)

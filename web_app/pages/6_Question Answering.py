import streamlit as st
import re
import pathlib

from ask_youtube_playlists.data_processing import EMBEDDING_MODELS_NAMES

st.set_page_config(
    page_title="Generative QA",
    page_icon="🧠",
)


def get_data_directory() -> pathlib.Path:
    """Returns the path to the data directory."""
    parent_path = pathlib.Path(__file__).parent
    while parent_path.name != "ask-youtube-playlists":
        parent_path = parent_path.parent

    data_directory = parent_path / "data"
    return data_directory


if "selected_playlists" not in st.session_state:
    st.session_state["selected_playlists"] = []

selected_playlists = st.session_state["selected_playlists"]
if "text" not in st.session_state:
    st.session_state["text"] = ""


def clear_text():
    st.session_state["text"] = ""


generative_models = ['GPT-3.5', 'GPT-4']
extractive_models = ['BERT', 'DistillBERT', 'RoBERTa']

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
                                        on_change=clear_text,
                                        key="generative_model")
    elif mode == 'extractive':
        extractive_model = st.selectbox("Select an Extractive Model",
                                        extractive_models,
                                        on_change=clear_text,
                                        key="extractive_model")
    st.header("Set hyperparameters")
    if mode == 'generative':
        # slider to choose temperature
        temperature = st.slider("Select Temperature",
                                min_value=0.0,
                                max_value=100.0,
                                value=50.0,
                                step=0.1)

        max_length = st.slider("Enter max_length value",
                               min_value=10,
                               max_value=8000,
                               value=50,
                               step=1)
    elif mode == 'extractive':
        n_returned_docs = st.slider("Select number of returned documents",
                                    min_value=1,
                                    max_value=100,
                                    value=5,
                                    step=1)

    # Set the playlist names on the sidebar
    st.subheader("Available Playlists")
    st.session_state["playlist_list"] = playlist_list
    # Allows to choose which playlists one wants to use
    for playlist in playlist_list:
        checkbox_value = st.checkbox(playlist)


# -----------------------------------------------------------------------------

# Function to get the answer based on the selected model
def get_answer(question, model):
    # [TODO] Implement the logic to retrieve the answer based on the
    #  selected model and mode
    if model == 'GPT-2':
        answer = 'Answer from GPT-2 extractive model'
    elif model == 'Llama':
        answer = 'Answer from Llama extractive model'
    elif model == 'T5':
        answer = 'Answer from T5 extractive model'

    return answer


def clear_text():
    st.session_state["generative_text"] = ""


# Question - Answering
def main():
    # Playlist selection, multiple playlists can be selected
    # From st.session_state["playlist_list"] create checkboxes
    # for each playlist
    for playlist in st.session_state["playlist_list"]:
        checkbox_value = st.checkbox(playlist, key=playlist)
        if st.session_state[playlist]:
            # Select the embeddings model
            embeddings = []
            # Iterate over the folders in the folder of the selected playlist
            for folder in get_data_directory() / playlist:
                # Check if the folder is a folder
                if folder.is_dir() and folder.name != "raw":
                    embeddings.append(folder.name)
            embeddings = st.radio("Select an Embeddings Model",
                                  embeddings,
                                  key="embeddings_model_" + playlist)

    # Receive question input
    question = st.text_input("Enter your question",
                             key="question")

    # the question must finish with an interrogation point
    if re.match(r".+\?$", question):
        # Answer display
        # TODO send question to the model
        # TODO display the answer from the model
        answer_generative = get_answer(question, model)
        st.write("Answer:", answer_generative)

        # Button to make another question
        st.button("I want to make another question", on_click=clear_text)
    else:
        st.error("Please Insert a question")


if __name__ == "__main__":
    main()

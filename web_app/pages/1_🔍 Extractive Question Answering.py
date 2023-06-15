import streamlit as st
import re  # regex library

from ask_youtube_playlists.data_processing import EMBEDDING_MODELS_NAMES


st.set_page_config(
    page_title="Extractive QA",
    page_icon="🔍",
)

st.title("Extractive Question Answering")

# Sidebar ---------------------------------------------------------------------
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

    num_docs = st.slider("Select Number of Documents to Retrieve",
                         min_value=1,
                         max_value=10,
                         value=5,
                         step=1)

    st.subheader("Available Playlists")
    playlist_list = st.session_state["loaded_playlist_names"]
    # Allows to choose which playlists one wants to use
    for playlist in playlist_list:
        checkbox_value = st.checkbox(playlist)


# ------------------------------------------------------------------------------

# Function to get the answer based on the selected model
def get_answer(question, model):
    # [TODO] Implement the logic to retrieve the answer based on the

    #  selected model and mode
    if model == 'BERT':
        answer = 'Answer from BERT extractive model'
    elif model == 'DistillBERT':
        answer = 'Answer from DistillBERT extractive model'
    elif model == 'RoBERTa':
        answer = 'Answer from RoBERTa extractive model'

    return answer


def clear_text():
    st.session_state["extractive_text"] = ""


# Define the available models for each mode
# TODO add the correct models we are going to use
extractive_models = ['BERT', 'DistillBERT', 'RoBERTa']


def main():

    # the user can only insert a question if the link is valid
    extractive_model = st.selectbox("Select an Extractive Model",
                                    extractive_models,
                                    key="extractive_model")

    # Receive question input
    question_extractive = st.text_input("Enter your question",
                                        key="extractive_text")

    # the question must finish with an interrogation point
    if re.match(r".+\?$", question_extractive):
        # Answer display
        # TODO send question to the model
        # TODO display the answer from the model
        answer_extractive = get_answer(question_extractive, extractive_model)
        st.write("Answer:", answer_extractive)

        # Button to make another question
        if question_extractive != "":
            st.button("I want to make another question", on_click=clear_text)
    else:
        st.error("Please Insert a question")


if __name__ == "__main__":
    main()

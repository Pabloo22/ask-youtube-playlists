import streamlit as st
import re  # regex library
from Load import playlist_list

st.set_page_config(
    page_title="Extractive QA",
    page_icon="🔍",
)

st.title("Extractive Question Answering")

# Sidebar ------------------------------------------------------------------------------- 
with st.sidebar:
    st.markdown("""
            <style>
            .sidebar .sidebar-content {
                min-width: 180px;
            }
            </style>
        """, unsafe_allow_html=True)
    
    # Set the playlist names on the sidebar
    st.subheader("Available Playlists")
    st.session_state["playlist_list"] = playlist_list
    # Allows to choose which playlists one wants to use
    for playlist in playlist_list:
        playlist_name = playlist["playlist_name"]
        checkbox_value = st.checkbox(playlist_name) 
#---------------------------------------------------------------------------------------

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
    extractive_model = st.radio("Select an Extractive Model", extractive_models,
                    on_change=clear_text)

        # Receive question input
    question_extractive = st.text_input("Enter your question", key="extractive_text")

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


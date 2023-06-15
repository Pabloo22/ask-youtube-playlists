import streamlit as st
import re  # regex library

st.set_page_config(
    page_title="Generative QA",
    page_icon="🧠",
)
playlist_list = st.session_state["loaded_playlist_names"]
st.title("Generative Question Answering")

# Sidebar ---------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
            <style>
            .sidebar .sidebar-content {
                min-width: 180px;
            }
            </style>
        """, unsafe_allow_html=True)

    st.header("Set hyperparameters")
    # box to insert max_length value
    max_length = st.number_input("Enter max_length value",
                                 min_value=0,
                                 max_value=100,
                                 value=50,
                                 step=1)
    # slider to choose temperature
    temperature = st.slider("Select Temperature",
                            min_value=0.0,
                            max_value=100.0,
                            value=50.0,
                            step=0.1)

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


# Define the available models for each mode
# TODO add the correct models we are going to use
generative_models = ['GPT-3.5', 'GPT-4']


# Question - Answering
def main():
    # the user can only insert a question if the link is valid
    generative_model = st.selectbox("Select a Generative Model",
                                    generative_models,
                                    on_change=clear_text,
                                    key="generative_model")

    # Receive question input
    question_generative = st.text_input("Enter your question",
                                        key="generative_text")

    # the question must finish with an interrogation point
    if re.match(r".+\?$", question_generative):
        # Answer display
        # TODO send question to the model
        # TODO display the answer from the model
        answer_generative = get_answer(question_generative, generative_model)
        st.write("Answer:", answer_generative)

        # Button to make another question
        st.button("I want to make another question", on_click=clear_text)
    else:
        st.error("Please Insert a question")


if __name__ == "__main__":
    main()

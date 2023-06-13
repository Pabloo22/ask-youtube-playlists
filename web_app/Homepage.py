import streamlit as st
import re # regex library

######### youtube playlist link to test: https://www.youtube.com/playlist?list=PLPNW_gerXa4Pc8S2qoUQc5e8Ir97RLuVW  ###############

st.set_page_config(
    page_title="Ask Youtube Playlist",
    page_icon="🔎",
)
st.title("Ask YouTube Playlist")

st.caption("Welcome to Ask YouTube Playlist! Get started by entering a valid YouTube playlist link below and selecting your preferred answering mode and model. Ask away and explore the content of your favorite YouTube playlists in a whole new way!")

# Define the question answering modes
modes = ['Extractive', 'Abstractive']

# Define the available models for each mode
#TODO add the correct models we are going to use
extractive_models = ['BERT', 'DistillBERT', 'RoBERTa']
abstractive_models = ['GPT-2', 'Llama', 'T5']

# Function to get the answer based on the selected model and mode
def get_answer(question, mode, model):
    #[TODO] Implement the logic to retrieve the answer based on the selected model and mode
    if mode == 'Extractive':
        if model == 'BERT':
            answer = 'Answer from BERT extractive model'
        elif model == 'DistillBERT':
            answer = 'Answer from DistillBERT extractive model'
        elif model == 'RoBERTa':
            answer = 'Answer from RoBERTa extractive model'
    elif mode == 'Abstractive':
        if model == 'GPT-2':
            answer = 'Answer from GPT-2 abstractive model'
        elif model == 'Llama':
            answer = 'Answer from Llama abstractive model'
        elif model == 'T5':
            answer = 'Answer from T5 abstractive model'
    return answer

# checks if a string is a youtube playlist link
def is_youtube_playlist(link):
    pattern = r'(https?://)?(www\.)?youtube\.com/playlist\?list=([a-zA-Z0-9_-]+)'
    match = re.match(pattern, link)
    return match is not None

def clear_text():
    st.session_state["text"] = ""

# Streamlit app
def main():
    # input for YouTube playlist link
    youtube_link = st.text_input("Enter YouTube Playlist Link")

    # the user can only insert a question if the link is valid
    if is_youtube_playlist(youtube_link):
        st.success("Valid YouTube playlist link!")
        # Mode selection
        mode = st.radio("Select Question Answering Mode", modes, on_change=clear_text)
        # Model selection based on the chosen mode
        if mode == 'Extractive':
            model = st.radio("Select an Extractive Model", extractive_models, on_change=clear_text)
        elif mode == 'Abstractive':
            model = st.radio("Select an Abstractive Model", abstractive_models, on_change=clear_text)

        # Receive question input
        question = st.text_input("Enter your question", key = "text")

        # the question must finish with an interrogation point
        if re.match(r".+\?$", question):
            # Answer display
            #TODO send question to the model
            #TODO display the answer from the model
            answer = get_answer(question, mode, model)
            st.write("Answer:", answer)

            # Button to make another question
            st.button("I want to make another question", on_click=clear_text)
        else:
            st.error("Please Insert a question")
    else:
        st.error("Invalid YouTube playlist link!")

if __name__ == "__main__":
    main()


    

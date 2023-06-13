import streamlit as st

st.set_page_config(
    page_title="Concepts",
    page_icon="📚",
)

st.title("📚 Concepts")

st.header("Extractive QA")
st.caption("Extractive QA is a question-answering approach that focuses on "
           "extracting relevant information directly from a given text or "
           "context to provide answers. It involves analyzing the input "
           "text, such as a document or passage, and identifying the most "
           "appropriate snippets of text that contain the answer to a "
           "specific question. Extractive models employ techniques like text "
           "comprehension and information retrieval to understand the "
           "context and extract the most relevant information. The selected "
           "snippets are then presented as the answer to the user's "
           "question. Extractive QA is advantageous as it provides precise "
           "and verifiable answers based on existing information in the text.")

st.header("Abstractive QA")
st.caption("Abstractive QA is a question-answering approach that involves "
           "generating concise and informative answers based on a given text "
           "or context. Unlike extractive methods, which select and "
           "rearrange existing text snippets, abstractive models focus on "
           "understanding the context and generating new responses in a "
           "human-like manner. These models employ natural language "
           "generation techniques, including summarization and paraphrasing, "
           "to produce coherent and contextually relevant answers. "
           "Abstractive QA is particularly useful when the answer requires a "
           "deeper understanding of the input text or when the available "
           "information doesn't have a direct textual representation. It "
           "allows for more creative and nuanced answers, which can enhance "
           "user engagement and provide a broader perspective on the given "
           "topic.")

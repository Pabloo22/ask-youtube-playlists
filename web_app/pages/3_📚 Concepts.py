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

st.subheader("Max_Length")
st.caption("")

st.subheader("Temperature")
st.caption("In natural language processing (NLP), the temperature value is a "
            "parameter used in language generation models, particularly in models "
            "based on softmax probabilities. It is used to control the randomness and "
            "diversity of thegenerated text. When generating text using NLP models "
            "like GPT-3, GPT-2, or other language models, the models typically produce "
            "a probability distribution over the next word or token. The temperature "
            "parameter allows you to adjust the sensitivity of this distribution. "
            "A higher temperature value, such as 1.0, increases the randomness "
            "of the generated text. It makes the model more exploratory and "
            "likely to generate diverse and unexpected responses. This can result "
            "in more creative but potentially less coherent or relevant output. "
            "On the other hand, a lower temperature value, such as 0.5, decreases "
            "the randomness and makes the model more focused and deterministic. "
            "It makes the generated text more conservative and tends to produce more "
            "coherent and conservative responses. Choosing the appropriate temperature "
            "value depends on the specific use case and desired output. Higher values "
            "promote exploration and diversity, which can be useful in creative writing "
            "or generating alternative ideas. Lower values promote convergence and "
            "coherence, which can be beneficial for tasks like summarization or "
            "providing precise answers.")

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
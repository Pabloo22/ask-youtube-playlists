import pytest
from langchain.embeddings import base
from langchain import embeddings
from langchain.schema import Document
from langchain import vectorstores

import pathlib
import os

from ask_youtube_playlists.data_processing import (create_vectorstore,
                                                   save_vectorstore,
                                                   load_vectorstore)
from ask_youtube_playlists.question_answering.retrieve import retrieve


def test_retrieve():
    test_persist_directory = str(pathlib.Path("tests") / "test_db")
    # Clear the test directory if it exists
    if pathlib.Path(test_persist_directory).exists():
        os.system(f"rm -rf {test_persist_directory}")
        os.system(f"mkdir {test_persist_directory}")

    documents = [
        Document(page_content="The meaning of life is 42.",
                 metadata={'title': 'first'}),
        Document(page_content="It is sunny today, good life.",
                 metadata={'title': 'second'}),
        Document(page_content="I like trains.",
                 metadata={'title': 'third'}),
    ]
    test_persist_directory = str(pathlib.Path("tests") / "test_db")
    vector_store: vectorstores.Chroma = create_vectorstore(
        "msmarco-distilbert-base-tas-b",
        documents,
        vector_store_type="chroma-db",
        persist_directory=test_persist_directory)

    save_vectorstore(vector_store)
    loaded_vector_store = load_vectorstore(test_persist_directory)

    dict_vector_store = {'vector_store': vector_store}

    retrieved_document = retrieve("What is the meaning of life?",
                                  dict_vector_store,
                                  1)

    assert retrieved_document[0].document == documents[0]

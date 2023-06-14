from langchain.schema import Document

import pathlib
import dotenv
import os

from ask_youtube_playlists.data_processing import create_vectorstore
from ask_youtube_playlists.question_answering.retrieve import retrieve


def _load_dotenv():
    dotenv.load_dotenv(dotenv.find_dotenv())
    # Set the environment variables
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def _get_documents():
    documents = [
        Document(page_content="The meaning of life is 42.",
                 metadata={'title': 'first'}),
        Document(page_content="It is sunny today, good life.",
                 metadata={'title': 'second'}),
        Document(page_content="I like trains.",
                 metadata={'title': 'third'}),
    ]
    return documents


def _get_test_directory():
    test_persist_directory = str(pathlib.Path("tests") / "test_db")
    # Clear the test directory if it exists
    if pathlib.Path(test_persist_directory).exists():
        os.system(f"rm -rf {test_persist_directory}")
        os.system(f"mkdir {test_persist_directory}")
    return test_persist_directory


def test_retrieve():
    test_persist_directory = _get_test_directory()
    documents = _get_documents()
    vector_store = create_vectorstore(
        "msmarco-distilbert-base-tas-b",
        documents,
        vector_store_type="chroma-db",
        persist_directory=test_persist_directory)

    dict_vector_store = {'vector_store': vector_store}

    retrieved_document = retrieve("What is the meaning of life?",
                                  dict_vector_store,
                                  1)

    assert retrieved_document[0].document == documents[0]


# def test_openai_retriever():
#     _load_dotenv()
#     if os.getenv("OPENAI_API_KEY") is not None:
#         test_persist_directory = _get_test_directory()
#         documents = _get_documents()
#         vector_store = create_vectorstore(
#             "text-embedding-ada-002",
#             documents,
#             vector_store_type="chroma-db",
#             persist_directory=test_persist_directory)
#
#         dict_vector_store = {'vector_store': vector_store}
#
#         retrieved_document = retrieve("What is the meaning of life?",
#                                       dict_vector_store,
#                                       n_documents=1)
#
#         assert retrieved_document[0].document == documents[0]
#     else:
#         pytest.skip("OPENAI_API_KEY not set in environment variables.")

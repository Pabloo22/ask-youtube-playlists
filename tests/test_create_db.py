import pathlib
import os
import pytest
from langchain.schema import Document
from langchain import vectorstores


from ask_youtube_playlists.data_processing import (create_vectorstore,
                                                   save_vectorstore,
                                                   load_vectorstore)


def test_create_vectorstore():
    test_persist_directory = str(pathlib.Path("tests") / "test_db")
    # Clear the test directory if it exists
    if pathlib.Path(test_persist_directory).exists():
        os.system(f"rm -rf {test_persist_directory}")
        os.system(f"mkdir {test_persist_directory}")

    documents = [
        Document(page_content="This is the first document.",
                 metadata={'title': 'first'}),
        Document(page_content="This is the second document.",
                 metadata={'title': 'second'}),
        Document(page_content="This is the third document.",
                 metadata={'title': 'third'}),
    ]
    test_persist_directory = str(pathlib.Path("tests") / "test_db")
    vector_store: vectorstores.Chroma = create_vectorstore(  # type: ignore
        "msmarco-MiniLM-L-6-v3",
        documents,
        vector_store_type="chroma-db",
        persist_directory=test_persist_directory)

    save_vectorstore(vector_store)
    loaded_vector_store = load_vectorstore(test_persist_directory)

    # Check thad the loaded vector has the documents inside
    get_loaded_documents = loaded_vector_store.get()
    loaded_page_content = get_loaded_documents['documents']
    loaded_metadatas = get_loaded_documents['metadatas']
    loaded_documents = zip(loaded_page_content, loaded_metadatas)
    for doc_num, (page_content, metadata) in enumerate(loaded_documents):
        assert page_content == documents[doc_num].page_content
        assert metadata == documents[doc_num].metadata


if __name__ == "__main__":
    pytest.main(["-vv", "test_create_db.py"])

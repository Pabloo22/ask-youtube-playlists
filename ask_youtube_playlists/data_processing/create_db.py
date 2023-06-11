"""Creates the Vector database."""
from langchain.embeddings import base
from langchain import embeddings
from langchain.schema import Document
from langchain import vectorstores
import os
import json
from typing import List, Union, Optional


def get_embedding_model(model_type: str = "sentence-transformers", **kwargs) -> base.Embeddings:
    """Returns the embedding model.

    Args:
        model_type (str): The langchain model type.

    Raises:
        ValueError: If the model type is not supported.
    """

    object_mapper = {
        "sentence-transformers": embeddings.SentenceTransformerEmbeddings,
        # "openai": embeddings.OpenAIEmbeddings,
    }

    if model_type not in object_mapper:
        raise ValueError(f"Model type {model_type} is not supported.")

    embedding_model = object_mapper[model_type](**kwargs)
    return embedding_model


def create_vectorstore(embedding_model: base.Embeddings,
                       documents: List[Document],
                       vector_store_type: str = "chroma",
                       **kwargs) -> None:
    """Creates the local database.

    Args:
        embedding_model (Embeddings): Embedding function.
        documents (List[Document]): List of documents.
        vector_store_type (str): The vector store type.
        **kwargs: Additional arguments passed to the `from_documents` method.
    """

    object_mapper = {
        "chroma-db": vectorstores.Chroma,
        "in-memory": vectorstores.DocArrayInMemorySearch,
    }

    vectorstore = object_mapper[vector_store_type].from_documents(documents, embedding_model, **kwargs)
    return vectorstore


def read_json(json_path: Union[str, os.PathLike]) -> Union[List[dict], dict]:
    """Reads a json file and returns the data."""
    with open(json_path, "r", encoding="utf-8") as file:
        json_data = json.load(file)

    return json_data


def _extract_documents_from_list_of_dicts(json_data: List[dict], text_key: str = "text") -> List[Document]:
    """Extracts documents from a list of dictionaries."""
    documents = []
    for item in json_data:
        if text_key not in item:
            raise KeyError(f"Key {text_key} not found in item {item}.")
        text = item[text_key]
        metadata = {key: value for key, value in item.items() if key != text_key}
        document = Document(text, metadata)
        documents.append(document)

    return documents


def extract_documents_from_json(json_path: Union[str, os.PathLike], text_key: str = "text") -> List[Document]:
    """Reads a json file with the youtube video transcripts format and creates a list of documents.

    The json file should have the following format:
    [{
        "text": "This is the first video transcript.",
        "url": "https://www.youtube.com/watch?v=1234567890",
        "title": "First video transcript"
        "duration": 123,
        "start": 0,
    },
    {
        "text": "This is the second video transcript.",
        ...
    },
    ...]
    It must have at least the `text` field. The other fields are stored as metadata.

    Args:
        json_path (Union[str, os.PathLike]): Path to the json file.
        text_key (str): The key of the text field. Defaults to "text".

    Returns:
        List[Document]: List of documents.
    """

    json_data = read_json(json_path)
    documents = _extract_documents_from_list_of_dicts(json_data, text_key=text_key)
    return documents


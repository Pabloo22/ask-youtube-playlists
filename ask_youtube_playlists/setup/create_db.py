"""Creates the Vector database."""
from langchain.embeddings import base
from langchain import embeddings
from langchain.schema import Document
from langchain import vectorstores
import pathlib
from typing import List, Union, Optional


def get_embedding_model(model_type: str = "sentence-transformers",
                        **kwargs) -> base.Embeddings:
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


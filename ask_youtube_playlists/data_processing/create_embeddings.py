"""Functions to create the Vector database."""
import os
from dataclasses import dataclass

from typing import List, Union, Dict, Callable

from langchain.embeddings import base
from langchain import embeddings
from langchain.schema import Document
from langchain import vectorstores

from .utils import get_device

DocumentDict = Dict[str, Union[str, float]]
PathLike = Union[str, os.PathLike]

MODEL_TYPES = {
    "sentence-transformers": embeddings.SentenceTransformerEmbeddings,
    "openai": embeddings.OpenAIEmbeddings,
}


@dataclass
class EmbeddingModelSpec:
    """Class to store the specification of an embedding model.

    Attributes:
        model_name: The name of the embedding model.
        model_type: The type of the embedding model. Can be
            `sentence-transformers` or `openai`.
        max_seq_length: The maximum number of tokens the model can handle.
    """
    model_name: str
    model_type: str
    max_seq_length: int

    def __post_init__(self):
        if self.model_type not in MODEL_TYPES:
            raise ValueError(f"Model type {self.model_type} is not supported."
                             f" The supported model types are "
                             f"{list(MODEL_TYPES.keys())}.")


EMBEDDING_MODELS = [
    EmbeddingModelSpec(model_name="msmarco-MiniLM-L-6-v3",
                       model_type="sentence-transformers",
                       max_seq_length=512),
    EmbeddingModelSpec(model_name="msmarco-distilbert-base-v4",
                       model_type="sentence-transformers",
                       max_seq_length=512),
    EmbeddingModelSpec(model_name="msmarco-distilbert-base-tas-b",
                       model_type="sentence-transformers",
                       max_seq_length=512),
    EmbeddingModelSpec(model_name="text-embedding-ada-002",
                       model_type="openai",
                       max_seq_length=8191),
]

EMBEDDING_MODELS_NAMES = [embedding_model.model_name
                          for embedding_model in EMBEDDING_MODELS]


def get_embedding_model(embedding_model_spec: EmbeddingModelSpec,
                        ) -> base.Embeddings:
    """Returns the embedding model.

    Args:
        embedding_model_spec (EmbeddingModelSpec): The langchain model type.

    Raises:
        ValueError: If the model type is not supported.
    """

    if embedding_model_spec.model_type == "sentence-transformers":
        model_name = f"sentence-transformers/{embedding_model_spec.model_name}"
        device = get_device()
        model = embeddings.SentenceTransformerEmbeddings(
            model_name=model_name,
            model_kwargs={"device": device},
        )
    elif embedding_model_spec.model_type == "openai":
        model = embeddings.OpenAIEmbeddings(  # type: ignore
            model=embedding_model_spec.model_name,
        )
    else:
        raise ValueError(f"Model type {embedding_model_spec.model_type} is not"
                         f" supported. The supported model types are "
                         f"{list(MODEL_TYPES.keys())}.")
    return model


def get_embedding_spec(model_name: str) -> EmbeddingModelSpec:
    """Returns the embedding model specification.

    Args:
        model_name (str): The name of the embedding model.

    Raises:
        ValueError: If the model name is not supported.
    """
    for embedding_model_spec in EMBEDDING_MODELS:
        if embedding_model_spec.model_name == model_name:
            return embedding_model_spec

    supported_model_names = [embedding_model_spec.model_name
                             for embedding_model_spec in EMBEDDING_MODELS]
    raise ValueError(f"Model name {model_name} is not supported. The "
                     f"supported model names are {supported_model_names}.")


def create_vectorstore(embedding_model_name: str,
                       documents: List[Document],
                       vector_store_type: str = "in-memory",
                       **kwargs) -> vectorstores.VectorStore:
    """Returns a vector store that contains the vectors of the documents.

    Currently, it only supports "in-memory" mode. In the future, it may
    support "chroma-db" mode as well.

    Note:
        In order to be able to make the vector store persistent, the
        `vector_store_type` should be `chroma-db` and the `kwargs` should
        contain the `persist_directory` argument with the path to the directory
        where the vector store will be saved or loaded from. The
        `persist_directory` is where Chroma will store its database files on
        disk, and load them on start.

    Args:
        embedding_model_name (str): The name of the embedding model.
        documents (List[Document]): List of documents.
        vector_store_type (str): The vector store type. Can be `chroma-db` or
            `in-memory`.
        **kwargs: Additional arguments passed to the `from_documents` method.

    Raises:
        ValueError: If the `persist_directory` argument is not provided when
            the vector store type is `chroma-db`.
    """

    if vector_store_type == "chroma-db" and "persist_directory" not in kwargs:
        raise ValueError(
            "The `persist_directory` argument should be provided when the "
            "vector store type is `chroma-db`. If you want to use an in-memory"
            " vector store, set the `vector_store_type` argument to "
            "`in-memory`.")

    object_mapper: Dict[str, Callable] = {
        # "chroma-db": vectorstores.Chroma.from_documents,
        "in-memory": vectorstores.DocArrayInMemorySearch.from_documents,
    }
    embedding_model_spec = get_embedding_spec(embedding_model_name)
    embedding_model = get_embedding_model(embedding_model_spec)

    vectorstore = object_mapper[vector_store_type](
        documents, embedding_model, **kwargs
    )
    return vectorstore


def save_vectorstore(chroma_vectorstore: vectorstores.Chroma) -> None:
    """Makes the vectorstore persistent in the local disk.

    The vectorstore is saved in the persist directory indicated when the
    vectorstore was created.

    Args:
        chroma_vectorstore (VectorStore): The vectorstore.
    """
    chroma_vectorstore.persist()


def load_vectorstore(persist_directory: PathLike) -> vectorstores.Chroma:
    """Loads a vectorstore from the local disk.

    Args:
        persist_directory (Union[str, os.PathLike]): The directory where the
            vectorstore is saved.

    Returns:
        VectorStore: The Chroma vectorstore.
    """
    chroma_vectorstore = vectorstores.Chroma(
        persist_directory=str(persist_directory)
    )
    return chroma_vectorstore

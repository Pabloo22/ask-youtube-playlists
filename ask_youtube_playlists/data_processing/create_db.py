"""Functions to create the Vector database."""
import os
import pathlib
import json
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
                       vector_store_type: str = "chroma-db",
                       **kwargs) -> vectorstores.VectorStore:
    """Returns a vector store that contains the vectors of the documents.

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
        "chroma-db": vectorstores.Chroma.from_documents,
        "in-memory": vectorstores.DocArrayInMemorySearch.from_documents,
    }
    embedding_model_spec = get_embedding_spec(embedding_model_name)
    embedding_model = get_embedding_model(embedding_model_spec)

    vectorstore = object_mapper[vector_store_type](
        documents, embedding_model, **kwargs
    )
    return vectorstore


def _read_json(json_path: PathLike) -> List[DocumentDict]:
    """Reads a json file and returns the data."""
    with open(json_path, "r", encoding="utf-8") as file:
        json_data = json.load(file)

    return json_data


def extract_documents_from_list_of_dicts(json_data: List[dict],
                                         text_key: str = "text"
                                         ) -> List[Document]:
    """Extracts documents from a list of dictionaries."""
    documents = []
    for item in json_data:
        if text_key not in item:
            raise KeyError(f"Key {text_key} not found in item {item}.")
        text = item[text_key]
        metadata = {key: value for key, value in item.items() if
                    key != text_key}
        document = Document(page_content=text, metadata=metadata)
        documents.append(document)

    return documents


def _extract_documents_from_json(json_path: PathLike,
                                 text_key: str = "text") -> List[Document]:
    """Reads a json file with the YouTube video transcripts format and creates
    a list of documents.

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
    It must have at least the `text` field. The other fields are stored as
    metadata.

    Args:
        json_path (Union[str, os.PathLike]): Path to the json file.
        text_key (str): The key of the text field. Defaults to "text".

    Returns:
        List[Document]: List of documents.
    """

    json_data = _read_json(json_path)
    documents = extract_documents_from_list_of_dicts(json_data,
                                                     text_key=text_key)
    return documents


def _extract_json_files_from_directory(directory_path: PathLike,
                                       start_with: str = ""
                                       ) -> List[pathlib.Path]:
    """Extracts the json files path from a directory.

    Args:
        directory_path (Union[str, os.PathLike]): Path to the directory with
            the json files. Usually .../data/playlist_name/processed.
        start_with (str): The json files must start with this string. Defaults
            to "".
    """
    directory_path = pathlib.Path(directory_path)
    json_files = list(directory_path.glob(f"{start_with}*.json"))
    return json_files


def get_documents_from_directory(directory_path: Union[str, os.PathLike],
                                 start_with: str = "",
                                 text_key: str = "text") -> List[Document]:
    """Extracts the documents from a directory with json files.

    Deprecated. We should use the `extract_documents_from_list_of_dicts`.

    Args:
        directory_path (Union[str, os.PathLike]): Path to the directory with
            the json files. Usually .../data/playlist_name/processed.
        start_with (str): The json files must start with this string. Defaults
            to "".
        text_key (str): The key of the text field. Defaults to "text".
    """
    json_files = _extract_json_files_from_directory(directory_path,
                                                    start_with=start_with)
    documents = []
    for json_file in json_files:
        documents.extend(
            _extract_documents_from_json(json_file, text_key=text_key))

    return documents


def save_vectorstore(chroma_vectorstore: vectorstores.Chroma) -> None:
    """Makes the vectorstore persistent in the local disk.

    The vectorstore is saved in the persist directory indicated when the
    vectorstore was created.

    Args:
        chroma_vectorstore (VectorStore): The vectorstore.
    """
    chroma_vectorstore.persist()


def load_vectorstore(persist_directory: Union[str, os.PathLike]
                     ) -> vectorstores.Chroma:
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

"""Contains the functionality used to retrieve the most relevant documents
for a given question."""
import pathlib

from typing import List, NamedTuple

import numpy as np
import yaml

from langchain.schema import Document

from ask_youtube_playlists.data_processing import (
    get_embedding_model,
    get_documents_from_directory,
    load_embeddings,
)


class DocumentInfo(NamedTuple):
    """Class to store information about a document.

    Attributes:
        document: The document text or content.
        score: The relevance score of the document. The higher the
            score, the more relevant the document is. It is in the range
            [0, 1].
        playlist_name: The name of the playlist to which the document belongs.
    """
    document: Document
    score: float
    playlist_name: str


class Retriever:
    """Class to retrieve the most relevant documents for a given question."""

    def __init__(self,
                 retriever_directory: pathlib.Path,
                 config_filename: str = "hyperparams.yaml"):
        self.retriever_directory = retriever_directory

        self.embedding_model_name = ""
        self.max_chunk_size = None
        self.min_overlap_size = None
        self._load_config(config_filename)

        self.embedding_model = get_embedding_model(self.embedding_model_name)

        chunked_data_directory = retriever_directory / "chunked_data"
        self.documents = get_documents_from_directory(chunked_data_directory)

        embedding_directory = retriever_directory / "embeddings"
        self.video_embeddings = load_embeddings(embedding_directory)

    @property
    def total_number_of_documents(self) -> int:
        """Returns the total number of documents."""
        return sum(len(video) for video in self.documents)

    def _load_config(self, filename: str = "hyperparams.yaml"):
        """Loads the hyperparameters from a YAML file.

        Args:
            filename (str): The name of the YAML file.
        """
        path_to_config = self.retriever_directory / filename
        with open(path_to_config, "r") as file:
            config = yaml.safe_load(file)

        self.embedding_model_name = config["model_name"]
        self.max_chunk_size = config["max_chunk_size"]
        self.min_overlap_size = config["min_overlap_size"]

    @staticmethod
    def cosine_distance(question_embedding: np.ndarray,
                        document_embedding: np.ndarray) -> float:
        """Calculates the cosine distance between two vectors.

        Args:
            question_embedding (np.ndarray): The embedding of the question.
            document_embedding (np.ndarray): The embedding of the document.

        Returns:
            float: The cosine distance between the two vectors.
        """
        question_embedding_norm = np.linalg.norm(question_embedding)
        document_embedding_norm = np.linalg.norm(document_embedding)
        denominator = question_embedding_norm * document_embedding_norm
        return np.dot(question_embedding, document_embedding) / denominator

    def retrieve_from_playlist(self,
                               question: str,
                               n_documents: int) -> List[DocumentInfo]:
        """Retrieves the most relevant documents with their relevance score.

        Args:
            question (str): The question posed by the user.
            n_documents (int): The number of documents to retrieve.
        """
        n_documents = min(n_documents, self.total_number_of_documents)

        playlist_name = self.retriever_directory.parent.name

        question_embedding = self.embedding_model.embed_query(question)
        question_embedding = np.array(question_embedding)  # type: ignore

        document_infos = []
        for video_documents, video_embedding in zip(self.documents,
                                                    self.video_embeddings):
            iterator = zip(video_documents, video_embedding)
            for i, (document, document_embedding) in enumerate(iterator):
                if document.metadata["index"] != i:
                    raise ValueError("The index of the document does not match"
                                     " its position in the list.")

                score = 1 - self.cosine_distance(
                    question_embedding, document_embedding  # type: ignore
                )
                document_info = DocumentInfo(document=document,
                                             score=score,
                                             playlist_name=playlist_name)
                document_infos.append(document_info)

        document_infos.sort(key=lambda x: x.score, reverse=True)
        return document_infos[:n_documents]

    @classmethod
    def retrieve(cls,
                 retrievers: List['Retriever'],
                 question: str,
                 n_documents: int) -> List[DocumentInfo]:
        """Retrieves the most relevant documents with their score and
        the playlist they belong to.

        This function retrieves documents in two steps:

        1. Extracts the most relevant documents from each retriever in

        2. Ranks the retrieved documents from all retrievers and returns the
        most relevant ones, in addition to their score and the playlist
        they belong to.

        Args:
            retrievers (List[Retriever]): A list of retrievers.
            question (str): The question posed by the user.
            n_documents (int): The number of documents to retrieve.

        Returns:
            list: A list of named tuples, each containing the document, its
            score and the playlist it belongs to. The list is sorted in
            descending order by relevance score.
        """
        document_infos = []
        for retriever in retrievers:
            document_infos.extend(retriever.retrieve_from_playlist(
                question, n_documents
            ))

        document_infos.sort(key=lambda x: x.score, reverse=True)
        return document_infos[:n_documents]

"""Contains the functionality used to retrieve the most relevant documents
for a given question."""
import pathlib

import numpy as np
import yaml

from typing import Dict, List, NamedTuple, Tuple

from langchain import vectorstores
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
                 embedding_directory: pathlib.Path,
                 config_filename: str = "hyperparams.yaml"):
        self.embedding_directory = embedding_directory

        self.embedding_model_name = ""
        self.max_chunk_size = None
        self.min_overlap_size = None
        self._load_config(config_filename)

        self.embedding_model = get_embedding_model(self.embedding_model_name)

        playlist_directory = self.embedding_directory.parent
        chunked_data_directory = playlist_directory / "processed"
        self.documents = get_documents_from_directory(chunked_data_directory)

        self.video_embeddings = load_embeddings(self.embedding_directory)

    @property
    def total_number_of_documents(self) -> int:
        """Returns the total number of documents."""
        return sum(len(video) for video in self.documents)

    def _load_config(self, filename: str = "hyperparams.yaml"):
        """Loads the hyperparameters from a YAML file.

        Args:
            filename (str): The name of the YAML file.
        """
        path_to_config = self.embedding_directory / filename
        with open(path_to_config, "r") as file:
            config = yaml.safe_load(file)

        self.embedding_model_name = config["embedding_model_name"]
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

    def _get_similarities(self,
                          question_embedding: np.ndarray,
                          video_embedding: np.ndarray) -> List[float]:
        """Returns a list of relevance scores for each document in the
        video.

        The score should be in the range [0, 1], where 1 means that the
        document is very relevant to the question and 0 means that it is not
        relevant at all.

        Args:
            question_embedding (np.ndarray): The embedding of the question.
                The shape should be (embedding_size,).
            video_embedding (np.ndarray): The embedding of the video. The
                shape should be (n_documents_in_the_video, embedding_size).
        """
        scores = []
        for document_embedding in video_embedding:
            cosine_distance = self.cosine_distance(question_embedding,
                                                   document_embedding)
            scores.append(1 - cosine_distance)
        return scores

    def _get_most_relevant_documents(self,
                                     scores: List[List[float]],
                                     n_documents: int
                                     ) -> List[Tuple[Document, float]]:
        """Returns the most relevant documents with their relevance score.

        Args:
            scores (List[List[float]]): A list of lists of relevance scores.
                The outer list contains the relevance scores for each video.
                The inner list contains the relevance scores for each document
                in the video.
            n_documents (int): The number of documents to retrieve.
        """
        documents = []
        for video_documents, video_scores in zip(self.documents, scores):
            for document, score in zip(video_documents, video_scores):
                documents.append((document, score))

        documents.sort(key=lambda x: x[1], reverse=True)
        return documents[:n_documents]

    def _retrieve(self,
                  question: str,
                  n_documents: int) -> List[DocumentInfo]:
        """Retrieves the most relevant documents with their relevance score.

        Args:
            question (str): The question posed by the user.
            n_documents (int): The number of documents to retrieve.
        """
        n_documents = min(n_documents, self.total_number_of_documents)

        question_embedding = self.embedding_model.embed_query(question)
        question_embedding = np.array(question_embedding)

        scores = []
        for video_embedding in self.video_embeddings:
            video_scores = self._get_similarities(question_embedding,
                                                  video_embedding)
            scores.append(video_scores)

        documents = self._get_most_relevant_documents(scores, n_documents)
        playlist_name = self.embedding_directory.parent.name

        result = [DocumentInfo(document, score, playlist_name)
                  for document, score in documents]
        return result

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
            document_infos.extend(retriever._retrieve(question, n_documents))

        document_infos.sort(key=lambda x: x.score, reverse=True)
        return document_infos[:n_documents]


def retrieve(question: str,
             vectorstores_dict: Dict[str, vectorstores.VectorStore],
             n_documents: int) -> List[DocumentInfo]:
    """Deprecated.

    Retrieves the most relevant documents with their relevance score and
    the playlist they belong to.

    This function retrieves documents in two steps:

    1. Extracts the most relevant documents from each vectorstore in
    `vectorstores_dict`.

    2. Ranks the retrieved documents from all vectorstores and returns the
    most relevant ones, in addition to their relevance score and the playlist
    they belong to.

    Args:
        question (str): The question posed by the user.
        vectorstores_dict (Dict[str, langchain.vectorstores.VectorStore]): A
            dictionary mapping playlist names to their respective vectorstores.
        n_documents (int): The number of documents to retrieve.

    Returns:
        list: A list of named tuples, each containing the document, its
        relevance score and the playlist it belongs to. The list is sorted in
        descending order by relevance score.
    """
    retrieved_documents = []
    for playlist_name, vectorstore in vectorstores_dict.items():
        retrieval = vectorstore.similarity_search_with_relevance_scores(
            question, n_documents
        )
        for document, score in retrieval:
            retrieved_documents.append(DocumentInfo(document,
                                                    score,
                                                    playlist_name))

    # Sort the documents by relevance score
    retrieved_documents.sort(key=lambda x: x.score)
    return retrieved_documents[:n_documents]

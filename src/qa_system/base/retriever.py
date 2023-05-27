import abc
import numpy as np
from dataenforce import Dataset


QueryResultDataFrame = Dataset["score": float, "index": int]


class Retriever(abc.ABC):
    """Base class for Information Retrieval component of the application."""

    @abc.abstractmethod
    def encode(self, text: str) -> np.ndarray:
        """Converts text into a vector representation.

        This method should be overridden by subclasses to include specific preprocessing steps such as text cleaning,
        tokenization, and so on. The base class method does nothing and should be called with super().preprocess() in
        the overriding method.

        Args:
            text (str): The text to be preprocessed.

        Returns:
            np.ndarray: The vector representation of the text.
        """

    @abc.abstractmethod
    def query(self, question: str) -> QueryResultDataFrame:
        """Identifies relevant transcripts based on the user's question.

        Args:
            question (str): The user's question.

        Returns:
            QueryResultDataFrame: The dataframe containing the results of the query. It has two columns: score and
                index. The score is the similarity between the question and the transcript. The index is the
                index of the text transcript in the episode.
        """

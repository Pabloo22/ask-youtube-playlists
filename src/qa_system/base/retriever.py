import abc
import numpy as np
from dataenforce import Dataset
import torch
from typing import Union, List

from . import Episode


QueryResultDataFrame = Dataset["score": float, "index": int, "episode": int]


class Retriever(abc.ABC):
    """Base class for Information Retrieval component of the application."""

    @abc.abstractmethod
    def encode(self, text: str, return_tensor: bool = False) -> Union[np.ndarray, torch.Tensor]:
        """Converts text into a vector representation.

        This method should be overridden by subclasses to include specific preprocessing steps such as text cleaning,
        tokenization, and so on. The base class method does nothing and should be called with super().preprocess() in
        the overriding method.

        Args:
            text (str): The text to be preprocessed.
            return_tensor (bool): Whether to return a tensor or np.ndarray.

        Returns:
            np.ndarray: The vector representation of the text.
        """

    def load_episode(self):
        pass

    @abc.abstractmethod
    def query(self, question: torch.Tensor, ) -> QueryResultDataFrame:
        """Identifies relevant transcripts based on the user's question.

        Args:
            question (str): The user's question.

        Returns:
            QueryResultDataFrame: The pandas dataframe containing the results of the query. It has two columns: score
            and
                index. The score is the similarity between the question and the transcript. The index is the
                index of the text transcript in the episode.
        """

import abc
import pandas as pd
import pathlib
from typing import List, Union


class InformationRetriever(abc.ABC):
    """
    Base class for Information Retrieval component of the application.

    This class should be inherited by specific information retrieval
    models which will implement the methods for identifying relevant
    podcast transcripts based on a user's question.

    Attributes:
        data_path (Union[str, pathlib.Path]): Path to the dataset. It will consider all files in the directory
            that have the extension .csv.
    """

    def __init__(self, data_path: Union[str, pathlib.Path]):
        self.data_path = pathlib.Path(data_path)
        self.data = None

    def preprocess(self):
        """Preprocesses the data.

        This method should be overridden by subclasses to include specific preprocessing steps such as text cleaning,
        tokenization, and so on. The base class method does nothing and should be called with super().preprocess() in
        the overriding method.

        Returns:
            None
        """
        pass

    @abc.abstractmethod
    def retrieve(self, question: str) -> pd.DataFrame:
        """Identifies relevant transcripts based on the user's question.

        This is an abstract method that should be implemented by all subclasses. It takes a user's question and returns
        a subs

        Args:
            question (str): The user's question.

        Returns:
            context
        """

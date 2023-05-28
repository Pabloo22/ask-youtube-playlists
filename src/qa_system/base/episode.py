import numpy as np
import pandas as pd
from dataenforce import Dataset
from typing import Optional


TranscriptDataFrame = Dataset["timestamp": float, "text": object]
TimestampDataFrame = Dataset["timestamp": float, "section": object]
EpisodeDataFrame = Dataset[TranscriptDataFrame, "section": object]


class Episode:
    """Wrapper class for the pandas dataframe containing the episode data.

    Attributes:
        data (EpisodeDataFrame): The dataset. It has three columns: timestamp, text, and section.
        embeddings (np.ndarray): The embeddings of the episode.
    """

    def __init__(self, data: EpisodeDataFrame, embeddings: Optional[np.ndarray] = None):
        self.data = data
        self.embeddings = embeddings

    def get_context(self, start: float, end: Optional[float] = None) -> str:
        """Returns the context between two timestamps.

        Args:
            start (float): The start timestamp.
            end (float): The end timestamp. If None, the context will be returned from the start timestamp to the end

        Returns:
            context (str): The context.
        """
        raise NotImplementedError

    def collapse_into_passages(self, size: int) -> "Episode":
        """Collapses the episode into passages of a given size.

        Args:
            size (int): The size of the passages.

        Returns:
            Episode: The episode with the passages.
        """
        raise NotImplementedError

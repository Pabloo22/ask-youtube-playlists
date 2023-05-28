import pandas as pd
from dataenforce import Dataset
from typing import Optional


TranscriptDataFrame = Dataset["timestamp": float, "text": object]
TimestampDataFrame = Dataset["timestamp": float, "section": object]
EpisodeDataFrame = Dataset[TranscriptDataFrame, "section": object]


class Episode:
    """Wrapper class for the pandas dataframe containing the episode data.

    Attributes:
        data (EpisodeDataFrame): The dataset.
    """

    def __init__(self, data: EpisodeDataFrame):
        self.data = data

    def get_context(self, start: float, end: Optional[float] = None) -> str:
        """Returns the context between two timestamps.

        Args:
            start (float): The start timestamp.
            end (float): The end timestamp. If None, the context will be returned from the start timestamp to the end

        Returns:
            context (str): The context.
        """
        raise NotImplementedError

    def chunk(self, chunk_size: int) -> 'Episode':
        """Chunks the episode into smaller episodes.

        Args:
            chunk_size (int): The size of each chunk in characters.

        Returns:
            Episode: The chunked episode.
        """
        raise NotImplementedError

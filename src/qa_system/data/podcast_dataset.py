import pathlib
from typing import Union


class PodcastDataset:
    """Wrapper class for the podcast dataset.

    The data have the following columns:
        - episode_num (int): The episode number.
        - episode_title (str): The episode title.
        - sentence (str): The sentence.
        - timestamp_start (float): The timestamp of the start of the sentence in seconds.
    """

    def __init__(self, data_path: Union[str, pathlib.Path]):
        self.data_path = data_path
        self.data = None

    def get_context(self, start: float, end: float) -> str:
        """Returns the context between two timestamps.

        Args:
            start (float): The start timestamp.
            end (float): The end timestamp.

        Returns:
            context (str): The context.
        """
        raise NotImplementedError

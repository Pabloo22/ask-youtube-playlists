"""Facade class that uses the Question Answering system"""
import pathlib


class AskYoutubePlaylist:

    def __init__(self,
                 data_path: pathlib.Path):
        """Initializes the AskYoutubePlaylist class.

        Args:
            data_path (pathlib.Path): Path to the data.
        """
        self.data_path = data_path

"""Utility functions for data processing."""
import pathlib
import re

from typing import List


def is_youtube_playlist(link) -> bool:
    """Checks if a string is a YouTube playlist link."""
    pattern = r'(https?://)?(www\.)?youtube\.com/playlist\?list=([' \
              r'a-zA-Z0-9_-]+)'
    match = re.match(pattern, link)
    return match is not None


def get_device() -> str:
    """Returns 'cuda' if a GPU is available, otherwise 'cpu'."""
    # import torch
    # return "cuda" if torch.cuda.is_available() else "cpu"
    # Currently, the model is too big to fit in the GPU memory for a RAM of 4GB
    # Maybe this can be fixed in the future
    return "cpu"


def get_available_playlist(data_directory: pathlib.Path) -> List[str]:
    """Returns a list of the available playlists.

    The playlists are the names of the directories in the data directory.
    """
    available_playlists = [playlist.name
                           for playlist in data_directory.iterdir()]
    return available_playlists


def load_playlist_vectorstore(playlist_directory: pathlib.Path,
                              embedding_model_name: str) -> None:
    """Loads the playlist vectorstore."""

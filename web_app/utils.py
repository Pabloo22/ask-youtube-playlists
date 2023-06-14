import pathlib

from typing import List


def get_data_directory() -> pathlib.Path:
    """Returns the path to the data directory."""
    parent_path = pathlib.Path(__file__).parent
    while parent_path.name != "ask-youtube-playlists":
        parent_path = parent_path.parent

    data_directory = parent_path / "data"
    return data_directory


def get_available_playlist(data_directory: pathlib.Path) -> List[str]:
    """Returns a list of the available playlists.

    The playlists are the names of the directories in the data directory.
    """
    data_directory = get_data_directory()
    available_playlists = [playlist.name
                           for playlist in data_directory.iterdir()]
import pathlib


def get_data_directory() -> pathlib.Path:
    """Returns the path to the data directory."""
    parent_path = pathlib.Path(__file__).parent
    while parent_path.name != "ask-youtube-playlists":
        parent_path = parent_path.parent

    data_directory = parent_path / "data"
    return data_directory

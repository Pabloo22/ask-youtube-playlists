import pytest
import pathlib

from ask_youtube_playlists.data_processing import get_available_directories


def _get_data_directory() -> pathlib.Path:
    """Returns the path to the data directory."""
    parent_path = pathlib.Path(__file__).parent
    while parent_path.name != "ask-youtube-playlists":
        parent_path = parent_path.parent

    data_directory = parent_path / "tests" / "data2"
    return data_directory


def test_get_available_playlist():
    data_dir = _get_data_directory()
    available_playlists = get_available_directories(data_dir)
    expected = {"playlist_name_1", "playlist_name_2"}
    assert set(available_playlists) == expected


if __name__ == "__main__":
    pytest.main()

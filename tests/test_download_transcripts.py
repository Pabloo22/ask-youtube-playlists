import pathlib
import json

import pytest

from ask_youtube_playlists.data_processing.download_transcripts import (
    _get_playlist_info,
    download_transcript,
    download_playlist,
    _replace_newlines,
    create_chunked_data
)


def test_get_playlist_info():
    # Test case for a valid playlist
    base_url = "https://www.youtube.com/playlist?list="
    url = base_url + "PLeKd45zvjcDFUEv_ohr_HdUFe97RItdiB"
    video_id_dict = _get_playlist_info(url)
    assert isinstance(video_id_dict, dict)
    assert len(video_id_dict) == 23

    # Test case for an invalid playlist
    url = base_url + "PLeKd45zvjcDFUEv_ohr_HdUFe97RItdiB_invalid"
    video_id_dict = _get_playlist_info(url)
    assert isinstance(video_id_dict, dict)
    assert len(video_id_dict) == 0


def test_download_transcript():
    video_title = "Test video"
    video_id = "slUCmZJDXrk"
    data_path = pathlib.Path("tests/data3")
    output_file = data_path / "raw" / "test.json"
    print(output_file)
    download_transcript(video_title, video_id, output_file, video_index=0,
                        verbose=False)
    assert output_file.exists()

    with open(output_file, 'r') as file:
        json_file_test = json.load(file)

    with open(data_path / 'raw' / 'example_download.json', 'r') as file:
        json_file_example = json.load(file)

    assert json_file_test == json_file_example

    # Clean up
    output_file.unlink()


def test_download_playlist():
    base_url = "https://www.youtube.com/playlist?list="
    url = base_url + "PLeKd45zvjcDFUEv_ohr_HdUFe97RItdiB"
    data_path = pathlib.Path("tests/data")
    download_playlist(url, data_path)

    for i in range(23):
        assert (data_path / f"Video_{i + 1}.json").exists()
        (data_path / f"Video_{i + 1}.json").unlink()


def test__replace_newlines():
    json_file = {
        "transcript": [
            {
                "text": "This is a test\n"
            },
            {
                "text": "This is another test\n"
            }
        ]
    }
    _replace_newlines(json_file)
    assert json_file["transcript"][0]["text"] == "This is a test "
    assert json_file["transcript"][1]["text"] == "This is another test "


def test_create_chunked_data():
    data_path = pathlib.Path("tests/data3")
    file_path = data_path / "raw" / "example_download.json"
    max_chunk_size = 200
    min_overlap_size = 50
    chunked_data = create_chunked_data(file_path,
                                       max_chunk_size,
                                       min_overlap_size)
    with open(data_path / 'raw' / 'example_chunked.json', 'r') as file:
        chunked_data_example = json.load(file)
    assert chunked_data == chunked_data_example

    def find_overlap_len(str1, str2):
        max_overlap_len = min(len(str1), len(str2))
        assert max_overlap_len != 0
        for overlap in range(max_overlap_len, 0, -1):
            if str1[-overlap:] == str2[:overlap]:
                return overlap

    for (i, chunk) in enumerate(chunked_data):
        assert len(chunk["text"]) <= max_chunk_size
        if i > 0:
            assert find_overlap_len(chunked_data[i - 1]["text"],
                                    chunk["text"]) >= min_overlap_size


if __name__ == "__main__":
    pytest.main(['-vv', 'test_download_transcripts.py'])

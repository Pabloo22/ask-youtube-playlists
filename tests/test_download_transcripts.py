import pathlib
import json

import pytest

from ask_youtube_playlists.data_processing.download_transcripts import (
    _get_playlist_info,
    download_transcript,
    download_playlist,
    _replace_newlines,
    create_chunked_data,
    _get_chunk_indices,
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

    def find_overlap_len(str1, str2):
        max_overlap_len = min(len(str1), len(str2))
        assert max_overlap_len != 0
        for overlap in range(max_overlap_len, 0, -1):
            if str1[-overlap:] == str2[:overlap]:
                return overlap

        print(str1)
        print(str2)

    for (i, chunk) in enumerate(chunked_data):
        assert len(chunk["text"]) <= max_chunk_size
        if i > 0:
            assert find_overlap_len(chunked_data[i - 1]["text"],
                                    chunk["text"]) >= min_overlap_size


def test__get_chunk_indices():
    sequence_lens = [10, 20, 10, 20, 10, 20, 10, 20, 10]
    # First chunk: 0 (10), 1 (20), 2 (10) = 40 + 2 = 42 <= 55
    # Overlap: 1 (20), 2 (10) = 30 + 1 = 31 >= 15
    # Second chunk: 1 (20), 2 (10), 3 (20) = 50 + 2 = 52 <= 55
    # Overlap: 3 (20) = 20 + 1 = 21 >= 15
    # Third chunk: 3 (20), 4 (10), 5 (20) = 50 + 2 = 52 <= 55
    # Overlap: 5 (20) = 20 + 1 = 21 >= 15
    # Fourth chunk: 5 (20), 6 (10), 7 (20) = 50 + 2 = 52 <= 55
    # Overlap: 7 (20) = 20 + 1 = 21 >= 15
    # Fifth chunk: 7 (20), 8 (10) = 30 + 2 = 32 <= 55

    max_chunk_size = 55
    min_overlap_size = 15
    chunk_indices = _get_chunk_indices(sequence_lens,
                                       max_chunk_size,
                                       min_overlap_size)
    assert chunk_indices == [(0, 2), (1, 3), (3, 5), (5, 7), (7, 8)], \
        f"chunk_indices: {chunk_indices}"


if __name__ == "__main__":
    pytest.main(['-vv', 'test_download_transcripts.py'])

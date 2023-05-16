import os
import pytest

from qa_system.data import filter_episode_transcript


def test_filter_episode_transcript():
    """Filters out the timestamps from the raw episode transcript."""

    # Get the directory of this file
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Read data/raw_data_example.txt
    with open(os.path.join(dir_path, "data/raw_data_example.txt"), "r") as f:
        raw_episode_transcript = f.read()

    # Read data/processed_data_example.txt
    with open(os.path.join(dir_path, "data/processed_data_example.txt"), "r") as f:
        processed_episode_transcript = f.read()

    assert filter_episode_transcript(raw_episode_transcript) == processed_episode_transcript


if __name__ == "__main__":
    pytest.main(["-vv", __file__])

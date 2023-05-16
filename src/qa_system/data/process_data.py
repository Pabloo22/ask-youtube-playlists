"""Filters the Episode-i.txt files from the data/raw/transripts folder and saves them
to data/processed/transcripts folder.

These text files follow the format:
0.0 ANDREW HUBERMAN: Welcome to
the Huberman Lab podcast,
2.22 where we discuss science
and science-based tools
4.89 for everyday life.
9.13 I'm Andrew Huberman,
and I'm a professor
...

This script filters out the timestamps. The expected output is:
ANDREW HUBERMAN: Welcome to
the Huberman Lab podcast,
where we discuss science
and science-based tools
for everyday life.
I'm Andrew Huberman,
and I'm a professor
...
"""
import dotenv
import os
import re

from .load_data import load_raw_episode_transcript


def filter_episode_transcript(raw_episode_transcript: str) -> str:
    """Filters out the timestamps from the raw episode transcript.

    Args:
        raw_episode_transcript (str): The raw episode transcript.

    Returns:
        filtered_episode_transcript (str): The filtered episode transcript.
    """



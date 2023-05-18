import re


def filter_episode_transcript(raw_episode_transcript: str, separator=r"\t") -> str:
    """Filters the Episode-i.txt files from the data/raw/transcripts folder and saves them
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
    0.0\tANDREW HUBERMAN: Welcome to the Huberman Lab podcast,
    2.22\twhere we discuss science and science-based tools
    4.89\tfor everyday life.
    9.13\tI'm Andrew Huberman, and I'm a professor
    ...

    Args:
        raw_episode_transcript (str): The raw episode transcript.
        separator (str): The separator between the timestamp and the sentence.

    Returns:
        filtered_episode_transcript (str): The filtered episode transcript.
    """
    split_newline = raw_episode_transcript.split("\n")
    filtered_episode_transcript = ""
    for line in split_newline:
        # Remove the brackets and the text inside them.
        line = re.sub(r"\[(.*?)\]", "", line)
        # If the line is empty, skip it.
        if re.match(r"^\d+.\d+ $", line):
            continue
        # If the line starts with a timestamp, add a new line.
        if re.match(r"^\d+.\d+", line):
            filtered_episode_transcript += "\n"
        else:
            filtered_episode_transcript += " "
        # Remove the space after the timestamp.
        line = re.sub(r"(\d+.\d+)\s", fr"\1{separator}", line)
        filtered_episode_transcript += line

    return filtered_episode_transcript[1:]  # Remove the first newline.

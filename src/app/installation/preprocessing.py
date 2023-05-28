import dotenv
import numpy as np
import pandas as pd
import os
import pathlib
import re

from qa_system.base import Retriever, TranscriptDataFrame, TimestampDataFrame, Episode, EpisodeDataFrame


NUMBER_OF_EPISODES = 95


def get_directory(directory: str = "data") -> pathlib.Path:
    """Returns the project directory containing the .env file.

    Args:
        directory: The directory containing the .env file. Can be set to
            "data" or "models", which will be mapped to
            "DATA_DIR" and "MODELS_DIR" respectively.

    Returns:
        pathlib.Path: The path to the directory.

    Raises:
        ValueError: If the directory does not exist in the .env file.
    """
    mapper = {
        "data": "DATA_DIR",
        "models": "MODELS_DIR",
    }
    if directory in mapper:
        directory = mapper[directory]

    dotenv.load_dotenv()
    directory = os.getenv(directory)

    if directory is None:
        raise ValueError(f"Variable '{directory}' does not exist in .env file.")

    return pathlib.Path(directory)


def _add_separator(raw_episode_transcript: str, separator=r"\t") -> str:
    """Adds a separator between the timestamp and the sentence and removes tags.

    These text files follow the format:
    0.0 ANDREW HUBERMAN: Welcome to
    the Huberman Lab podcast,
    2.22 where we discuss science
    and science-based tools
    4.89 for everyday life.
    9.13 I'm Andrew Huberman,
    and I'm a professor
    ...

    The expected output is:
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


def _get_transcript_dataset(transcript_text: str) -> TranscriptDataFrame:
    """Returns a dataframe containing the transcript data.

    Args:
        transcript_text: The transcript text.
    """
    # Add a separator between the timestamp and the sentence.
    transcript_text = _add_separator(transcript_text)
    # Split the text into lines.
    transcript_lines = transcript_text.split("\n")
    # Split the lines into columns.
    transcript_columns = [line.split("\t") for line in transcript_lines]
    # Create the dataframe.
    transcript_dataset = pd.DataFrame(transcript_columns, columns=["timestamp", "text"])

    return transcript_dataset

def _convert_to_seconds(time):
    time = time.split(':')
    return int(time[0])*3600 + int(time[1])*60 + int(time[2])

def _get_timestamp_dataset(timestamp_text: str) -> TimestampDataFrame:
    """Returns a dataframe containing the timestamp data.

    Args:
        timestamp_text: The timestamp text.
    """
    # Split the text into lines.
    timestamp_lines = timestamp_text.split("\n")
    # Split the lines into columns.
    timestamp_columns = [[_convert_to_seconds(line.split(" ")[0]),
                          " ".join(line.split(" ")[1:])] for line in timestamp_lines]
    # Create the dataframe.
    timestamp_dataset = pd.DataFrame(timestamp_columns, columns=["timestamp", "section"])

    return timestamp_dataset


def _merge(transcript_dataset: TranscriptDataFrame, timestamp_dataset: TimestampDataFrame) -> EpisodeDataFrame:
    """Merges the transcript and timestamp datasets.

    Args:
        transcript_dataset: The transcript dataset.
        timestamp_dataset: The timestamp dataset.
    """
    merged_dataset = transcript_dataset.copy()
    # Add the section column
    merged_dataset['section'] = None

    for i in range(len(timestamp_dataset)-1):
        # Get the timestamps
        start = timestamp_dataset.iloc[i]['timestamp']
        end = timestamp_dataset.iloc[i+1]['timestamp']
        # Get the section
        section = timestamp_dataset.iloc[i]['section']
        # Get the indices of the rows that have the timestamps between the start and the end
        indices = transcript_dataset[(transcript_dataset['timestamp'] >= start) &
                                     (transcript_dataset['timestamp'] < end)].index
        # Add the section to the rows
        merged_dataset.loc[indices, 'section'] = section

    return merged_dataset

def _load_episode(transcript_path: pathlib.Path, timestamp_path: pathlib.Path) -> Episode:
    """Returns a dataframe containing the episode data.

    Args:
        transcript_path: The path to the transcript file.
        timestamp_path: The path to the timestamp file.
    """
    transcript_text = transcript_path.read_text()
    timestamp_text = timestamp_path.read_text()

    transcript_dataset = _get_transcript_dataset(transcript_text)
    timestamp_dataset = _get_timestamp_dataset(timestamp_text)

    episode_dataset = _merge(transcript_dataset, timestamp_dataset)

    return Episode(episode_dataset)


def _chunk_episode(episode_dataset: Episode, max_chunk_length: int) -> Episode:
    """Splits the episode into chunks.

    Args:
        episode_dataset: The episode dataset.
        max_chunk_length: The maximum length of a chunk in characters.
    """


def _encode_episode(episode_dataset: Episode, retriever: Retriever) -> np.ndarray:
    """Encodes the episode dataset using the retriever model.

    Args:
        episode_dataset: The episode dataset.
        retriever: The retriever model.
    """


def _episode_pipeline(transcript_path: pathlib.Path,
                      timestamp_path: pathlib.Path,
                      max_chunk_length: int,
                      retriever: Retriever) -> None:
    """Applies the full preprocessing pipeline to a single episode.

    1. Loads the episode data and creates a dataframe.
    2. Split the text into chunks.
    3. Saves the dataframes with the chunks to a .json file in the data/processed folder.
    4. Creates the vector data for the app and saves it to the data/embeddings folder.

    Args:
        transcript_path: The path to the transcript file.
        timestamp_path: The path to the timestamp file.
        max_chunk_length: The maximum length of a chunk in characters.
        retriever: The retriever model.
    """

    episode_dataset = _load_episode(transcript_path, timestamp_path)
    episode_dataset_chunked = _chunk_episode(episode_dataset, max_chunk_length)

    # Save the chunked episode dataset to a .json file.
    data_dir = get_directory("data")
    processed_dir = data_dir / "processed"
    episode_number = transcript_path.stem.split("-")[1]
    episode_path = processed_dir / f"Episode-{episode_number}.json"
    episode_dataset_chunked.data.to_json(episode_path)

    # Encode the episode dataset and save it to a .npy file.
    embeddings_dir = data_dir / "embeddings"
    episode_array = _encode_episode(episode_dataset_chunked, retriever)
    episode_vector_path = embeddings_dir / f"Episode-{episode_number}.npy"
    np.save(episode_vector_path, episode_array)


def preprocess_data(retriever: Retriever, max_chunk_length: int) -> None:
    """Applies the full preprocessing pipeline.

    This function is called from install_app.py.

    1. Loads the episode data and creates a dataframe.
    2. Split the text into chunks.
    3. Saves the dataframes with the chunks to a .json files in the data/processed folder.
    4. Creates the vector data for the app and saves it to the data/embeddings folder.

    Args:
        retriever: The retriever model.
        max_chunk_length: The maximum length of a chunk in characters.
    """
    data_dir = get_directory("data")
    raw_dir = data_dir / "raw"

    # Create the processed directory if it does not exist.
    processed_dir = data_dir / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    # Create the embeddings directory if it does not exist.
    embeddings_dir = data_dir / "embeddings"
    embeddings_dir.mkdir(parents=True, exist_ok=True)

    # Iterate over all episodes and apply the preprocessing pipeline.
    for episode_number in range(1, NUMBER_OF_EPISODES + 1):
        transcript_path = raw_dir / "transcripts" / f"Episode-{episode_number}.txt"
        timestamp_path = raw_dir / "timestamps" / f"Episode-{episode_number}.txt"
        _episode_pipeline(transcript_path, timestamp_path, max_chunk_length, retriever)

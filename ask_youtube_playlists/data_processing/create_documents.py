"""Contains functions to create documents from json files or
their corresponding python objects.
"""
import os
import json
import pathlib
from typing import List, Union, Dict

from langchain.schema import Document

DocumentDict = Dict[str, Union[str, float]]
PathLike = Union[str, os.PathLike]


def _read_json(json_path: PathLike) -> List[DocumentDict]:
    """Reads a json file and returns the data."""
    with open(json_path, "r", encoding="utf-8") as file:
        json_data = json.load(file)

    return json_data


def extract_documents_from_list_of_dicts(json_data: List[dict],
                                         text_key: str = "text"
                                         ) -> List[Document]:
    """Extracts documents from a list of dictionaries."""
    documents = []
    for item in json_data:
        if text_key not in item:
            raise KeyError(f"Key {text_key} not found in item {item}.")
        text = item[text_key]
        metadata = {key: value for key, value in item.items() if
                    key != text_key}
        document = Document(page_content=text, metadata=metadata)
        documents.append(document)

    return documents


def _extract_documents_from_json(json_path: PathLike,
                                 text_key: str = "text") -> List[Document]:
    """Reads a json file with the YouTube video transcripts format and creates
    a list of documents.

    The json file should have the following format:
    [{
        "text": "This is the first video transcript.",
        "url": "https://www.youtube.com/watch?v=1234567890",
        "title": "First video transcript"
        "duration": 123,
        "start": 0,
    },
    {
        "text": "This is the second video transcript.",
        ...
    },
    ...]
    It must have at least the `text` field. The other fields are stored as
    metadata.

    Args:
        json_path (Union[str, os.PathLike]): Path to the json file.
        text_key (str): The key of the text field. Defaults to "text".

    Returns:
        List[Document]: List of documents.
    """

    json_data = _read_json(json_path)
    documents = extract_documents_from_list_of_dicts(json_data,
                                                     text_key=text_key)
    return documents


def _extract_json_files_from_directory(directory_path: PathLike,
                                       start_with: str = ""
                                       ) -> List[pathlib.Path]:
    """Extracts the json files path from a directory.

    Args:
        directory_path (Union[str, os.PathLike]): Path to the directory with
            the json files. Usually .../data/playlist_name/processed.
        start_with (str): The json files must start with this string. Defaults
            to "".
    """
    directory_path = pathlib.Path(directory_path)
    json_files = list(directory_path.glob(f"{start_with}*.json"))
    return json_files


def get_documents_from_directory(directory_path: Union[str, os.PathLike],
                                 start_with: str = "",
                                 text_key: str = "text") -> List[Document]:
    """Extracts the documents from a directory with json files.

    Deprecated. We should use the `extract_documents_from_list_of_dicts`.

    Args:
        directory_path (Union[str, os.PathLike]): Path to the directory with
            the json files. Usually .../data/playlist_name/processed.
        start_with (str): The json files must start with this string. Defaults
            to "".
        text_key (str): The key of the text field. Defaults to "text".
    """
    json_files = _extract_json_files_from_directory(directory_path,
                                                    start_with=start_with)
    documents = []
    for json_file in json_files:
        documents.extend(
            _extract_documents_from_json(json_file, text_key=text_key))

    return documents

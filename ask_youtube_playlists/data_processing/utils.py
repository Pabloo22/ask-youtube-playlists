"""Utility functions for data processing."""
import os
import pathlib
import dotenv


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
    directory = mapper.get(directory, directory)

    dotenv.load_dotenv()
    directory = os.getenv(directory)  # type: ignore

    if directory is None:
        raise ValueError(f"Variable '{directory}' does not exist in "
                         f".env file.")

    return pathlib.Path(directory)

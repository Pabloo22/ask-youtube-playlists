"""Creates the vector data for the app."""
import os
import dotenv
import pathlib
import pandas as pd


def get_directory(directory: str = "data") -> pathlib.Path:
    """Returns the project directory containing the .env file.

    Args:
        directory: The directory containing the .env file. Can be set to
            "data" or "models".
    """
    variable_names_in_env = {
        "data": "DATA_DIR",
        "models": "MODELS_DIR",
    }
    if directory not in variable_names_in_env:
        raise ValueError(f"Directory {directory} not found. "
                         f"Valid directories are: {list(variable_names_in_env.keys())}")
    dotenv.load_dotenv()
    directory = os.getenv(variable_names_in_env[directory])
    return pathlib.Path(directory)


def load_episode(data_path: pathlib.Path) -> pd.DataFrame:
    """Returns a dataframe containing the episode data.

    The

    Args:
        data_path: The path to the dataset.
    """
    return pd.read_csv(data_path)
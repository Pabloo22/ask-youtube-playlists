import dotenv
import os
import pathlib


def load_raw_episode_transcript(episode_num: int) -> str:
    """Loads the raw data from the data/raw/transcripts folder.

    Returns:
        raw_data (str): The raw data.
    """
    dotenv.load_dotenv()
    raw_data_path = pathlib.Path(os.getenv("DATA_DIR")) / "raw" / "transcripts"

    raw_data = ""
    for file in raw_data_path.iterdir():
        if not file.name.startswith(f"Episode-{episode_num}"):
            continue
        with open(file, "r") as f:
            raw_data += f.read()

    return raw_data

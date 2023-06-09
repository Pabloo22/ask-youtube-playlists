"""Facade class that uses all the functions in the package."""
import pathlib


class AskYoutubePlaylist:

    def __init__(self,
                 data_path: pathlib.Path,
                 model_type: str = "sentence-transformers",
                 vector_store_type: str = "chroma"):
        """Initializes the AskYoutubePlaylist class.

        Args:
            data_path (pathlib.Path): Path to the data.
            model_type (str): The langchain model type.
            vector_store_type (str): The vector store type.
        """
        self.data_path = data_path
        self.model_type = model_type
        self.vector_store_type = vector_store_type

    def create_vector_store(self, name: str, youtube_playlist_url: str):
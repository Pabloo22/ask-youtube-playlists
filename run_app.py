"""Downloads the transcripts of the YouTube videos and creates the embeddings."""
import click
import pathlib
import yaml
from langchain import vectorstores
from typing import Optional

from app import setup


CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()
CONFIG_PATH = CURRENT_DIRECTORY / "configs"

EMBEDDINGS_MODEL_CONFIG_FILENAME = "embedding_model.yaml"
ABSTRACTIVE_QA_MODEL_CONFIG_FILENAME = "abstractive_qa_model.yaml"
EXTRACTIVE_QA_MODEL_CONFIG_FILENAME = "extractive_qa_model.yaml"


def _get_embedding_model_config(filename: str) -> dict:
    """Returns a dictionary containing the configuration for the embedding model."""
    return yaml.safe_load(open(CONFIG_PATH / filename))


def get_storage_path(directory: str, data_path: Optional[str] = None) -> pathlib.Path:
    data_path = setup.get_directory("data") if data_path is None else pathlib.Path(data_path)
    storage_path = data_path / directory if directory is not None else data_path
    return storage_path


def _load_vectorstore(directory: str, data_path: Optional[str] = None) -> vectorstores.VectorStore:
    storage_path = get_storage_path(directory, data_path)
    vectorstore = setup.load_vectorstore(storage_path)
    return vectorstore


def _load_videos(youtube_url: str) -> vectorstores.VectorStore:
    embedding_model_config = _get_embedding_model_config(EMBEDDINGS_MODEL_CONFIG_FILENAME)
    embeddings_model = setup.create_embeddings_model(embedding_model_config)
    vectorstore = setup.create_vector_store(youtube_url, embeddings_model)
    return vectorstore


def create_vectorstore(youtube_url: str,
                       persistent: bool = True,
                       storage_path: Optional[pathlib.Path] = None) -> vectorstores.VectorStore:
    """Runs the installation process."""

    vectorstore = _load_videos(youtube_url)
    if persistent:
        setup.save_vector_store(storage_path)


def get_vectorstore(directory: str = None, youtube_url: str = None, data_path: str = None) -> vectorstores.VectorStore:
    """Returns the vectorstore."""
    if directory is None:
        return create_vectorstore(youtube_url, persistent=False)

    storage_path = get_storage_path(directory, data_path)
    if not storage_path.exists():
        create_vectorstore(youtube_url, persistent=True, storage_path=storage_path)

    return _load_vectorstore(directory, data_path)


@click.command()
@click.option('--directory', default=None, help="Directory for vectorstore. If it doesn't exist, it will be created "
                                                "inside the data directory.")
@click.option('--youtube_url', default=None, help="URL of YouTube video or playlist")
@click.option('--data_path', default=None, help="Data path. There is no need to provide it,"
                                                " if it's already set in the .env file.")
def run_app(directory: Optional[str] = None,
            youtube_url: Optional[str] = None,
            data_path: Optional[str] = None):
    """Runs the app."""

    vectorstore = get_vectorstore(directory, youtube_url, data_path)
    extractive_qa_model_config = _get_embedding_model_config(EXTRACTIVE_QA_MODEL_CONFIG_FILENAME)
    abstractive_qa_model_config = _get_embedding_model_config(ABSTRACTIVE_QA_MODEL_CONFIG_FILENAME)

    setup.run_app(vectorstore, extractive_qa_model_config, abstractive_qa_model_config)


if __name__ == "__main__":
    run_app()

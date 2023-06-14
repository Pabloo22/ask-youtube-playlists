"""This module contains the functions related to the data.

These are the steps to follow:
1.- Download the transcripts of the videos in the playlists.
2.- Create chunks of data from the transcripts, where you can decide the size
of the chunks and the overlap between them.
3.- Create a vectorstore from the chunks of data.
"""
from .create_db import (get_embedding_model,
                        create_vectorstore,
                        get_documents_from_directory,
                        save_vectorstore,
                        load_vectorstore)

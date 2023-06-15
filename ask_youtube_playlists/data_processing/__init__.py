"""This module contains the functions related to the data.

These are the steps to follow:
1.- Download the transcripts of the videos in the playlists.
2.- Create chunks of data from the transcripts, where you can decide the size
of the chunks and the overlap between them.
3.- Create a vectorstore from the chunks of data.
"""
from .create_embeddings import (get_embedding_model,
                                create_vectorstore,
                                save_vectorstore,
                                load_vectorstore,
                                EMBEDDING_MODELS_NAMES,
                                get_embedding_spec
                                )

from .create_documents import (get_documents_from_directory,
                               extract_documents_from_list_of_dicts)

from .download_transcripts import (download_playlist,
                                   create_chunked_data,
                                   )

from .utils import (is_youtube_playlist,
                    get_device,
                    get_available_playlist,
                    )

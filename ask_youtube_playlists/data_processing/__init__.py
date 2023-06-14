"""This module contains the functions necessary to fully install the app.

The installation process consists of the following steps:
1. Download the models.
2. Preprocess the data.
3. Convert the data to vectors.
"""
from .create_db import (get_embedding_model,
                        create_vectorstore,
                        get_documents_from_directory,
                        save_vectorstore,
                        load_vectorstore,
                        EMBEDDING_MODELS_NAMES)

from .download_transcripts import (download_playlist,
                                   create_chunked_data,
                                   )

from .utils import (is_youtube_playlist,
                    get_device,
                    get_available_playlist,
                    )

"""This module contains the functions necessary to fully install the app.

The installation process consists of the following steps:
1. Download the models.
2. Preprocess the data.
3. Convert the data to vectors.
"""
from .create_db import get_embedding_model, get_vectorstore, get_documents_from_directory, save_vectorstore

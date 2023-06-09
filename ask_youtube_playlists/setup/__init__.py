"""This module contains the functions neccessary to fully install the app.

The installation process consists of the following steps:
1. Download the models.
2. Preprocess the data.
3. Convert the data to vectors.
"""
from .create_db import get_embedding_model, create_vectorstore

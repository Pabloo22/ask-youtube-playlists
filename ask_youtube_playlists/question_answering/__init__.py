"""Implements the question answering system.

It consists of three components:
1.- Retrieval: This component retrieves the most relevant documents for a given
question.

2.- Extractive: This component extracts the most relevant sentences from the
retrieved documents.

3.- Generative: This component generates an answer to the question from the
extracted sentences.
"""

from .extractive import EXTRACTIVE_MODEL_NAMES, get_extractive_answer
from .generative import GENERATIVE_MODEL_NAMES, get_generative_answer
from .retriever import Retriever

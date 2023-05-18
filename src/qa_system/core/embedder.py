import abc
import numpy as np


class Embedder(abc.ABC):
    """Base class for Embedding component of the application."""

    @abc.abstractmethod
    def embed(self, text: str) -> np.ndarray:
        """Embeds a text.

        This is an abstract method that should be implemented by all subclasses. It takes a text and returns
        its embedding.

        Args:
            text (str): The text to embed.

        Returns:
            np.ndarray: The embedding of the text.
        """

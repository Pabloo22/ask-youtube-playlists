import numpy as np
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util
from typing import Union, List

from qa_system.base import Retriever, QueryResultDataFrame, EpisodeDataFrame


class DistilBertRetriever(Retriever):
    """Retriever using DistilBert model."""

    def __init__(self, model_name: str = 'sentence-transformers/msmarco-distilbert-base-dot-v5',
                 number_of_retrieved_passages: int = 5,
                 score_threshold: float = 0.0):
        self.model = SentenceTransformer(model_name)
        self.number_of_retrieved_passages = number_of_retrieved_passages
        self.score_threshold = score_threshold

        # Use GPU if available
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self.model.to(self.device)

    def encode(self, text: str, return_tensor: bool = False) -> Union[torch.Tensor, np.ndarray]:
        """Converts text into a vector representation using DistilBert model.

        Args:
            text (str): The text to be encoded.
            return_tensor (bool): Whether to return a tensor or np.ndarray.

        Returns:
            Tensor or np.ndarray: The vector representation of the text.
        """
        encoded_text = self.model.encode(text, convert_to_tensor=return_tensor)
        if return_tensor:
            encoded_text = encoded_text.to(self.device)
        return encoded_text

    @staticmethod
    def query_episode(question: torch.Tensor, episode: torch.Tensor) -> List[float]:
        """Computes the dot scores for a question with all passages in an episode.

        Args:
            question (Tensor): The question tensor.
            episode (List[Tensor]): The list of passage tensors for an episode.

        Returns:
            List[float]: List of dot scores for all passages in the episode.
        """
        return util.dot_score(question, episode)[0].cpu().tolist()

    def query(self, question: torch.Tensor, episodes: List[torch.Tensor]) -> QueryResultDataFrame:
        """Identifies relevant passages across all episodes based on the user's question.

        Args:
            question (Tensor): The user's question tensor.
            episodes (List[List[Tensor]]): The list of episodes, where each episode is a list of passage tensors.

        Returns:
            QueryResultDataFrame: The dataframe containing the results of the query.
        """
        scores = []
        indices = []
        episode_numbers = []

        for episode_number, episode in enumerate(episodes, start=1):
            episode_scores = self.query_episode(question, episode)
            scores.extend(episode_scores)
            indices.extend(range(len(episode)))
            episode_numbers.extend([episode_number]*len(episode))

        df = self._create_dataframe(scores, indices, episode_numbers)
        return df

    @staticmethod
    def _create_dataframe(scores: List[float], indices: List[int], episode_numbers: List[int]) -> QueryResultDataFrame:
        """Creates a dataframe from the list of scores, indices, and episode numbers.

        Args:
            scores (List[float]): The list of scores.
            indices (List[int]): The list of passage indices.
            episode_numbers (List[int]): The list of episode numbers.

        Returns:
            QueryResultDataFrame: The dataframe with columns for score, index, and episode.
        """
        df = pd.DataFrame(dict(score=scores, index=indices, episode=episode_numbers))
        df.sort_values(by='score', ascending=False, inplace=True)
        return df

    def retrieve_relevant_passages(self, df: QueryResultDataFrame) -> QueryResultDataFrame:
        """Returns the most relevant rows based on the score.

        Args:
            df (QueryResultDataFrame): The dataframe containing scores, indices, and episode numbers.

        Returns:
            QueryResultDataFrame: The dataframe with most relevant rows.
        """
        relevant_df = df[df['score'] > self.score_threshold]
        relevant_df = relevant_df.head(self.number_of_retrieved_passages)
        return relevant_df

"""Contains the functionality used to retrieve the most relevant documents
for a given question."""

from typing import Dict, List, NamedTuple
from langchain import vectorstores
from langchain.schema import Document


class DocumentInfo(NamedTuple):
    """Class to store information about a document.

    Attributes:
        document: The document text or content.
        relevance_score: The relevance score of the document. The higher the
            score, the more relevant the document is. It is in the range
            [0, 1].
        playlist_name: The name of the playlist to which the document belongs.
    """
    document: Document
    relevance_score: float
    playlist_name: str


def retrieve(question: str,
             vectorstores_dict: Dict[str, vectorstores.VectorStore],
             n_documents: int) -> List[DocumentInfo]:
    """Retrieves the most relevant documents with their relevance score and
    the playlist they belong to.

    This function retrieves documents in two steps:

    1. Extracts the most relevant documents from each vectorstore in
    `vectorstores_dict`.

    2. Ranks the retrieved documents from all vectorstores and returns the
    most relevant ones, in addition to their relevance score and the playlist
    they belong to.

    Args:
        question (str): The question posed by the user.
        vectorstores_dict (Dict[str, langchain.vectorstores.VectorStore]): A
            dictionary mapping playlist names to their respective vectorstores.
        n_documents (int): The number of documents to retrieve.

    Returns:
        list: A list of named tuples, each containing the document, its
        relevance score and the playlist it belongs to. The list is sorted in
        descending order by relevance score.
    """
    retrieved_documents = []
    for playlist_name, vectorstore in vectorstores_dict.items():
        retrieval = vectorstore.similarity_search_with_relevance_scores(
            question, n_documents
        )
        for document, score in retrieval:
            retrieved_documents.append(DocumentInfo(document,
                                                    score,
                                                    playlist_name))

    # Sort the documents by relevance score
    retrieved_documents.sort(key=lambda x: x.relevance_score, reverse=True)
    return retrieved_documents[:n_documents]

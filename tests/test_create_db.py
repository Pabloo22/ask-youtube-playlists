import pytest
from langchain import embeddings

from ask_youtube_playlists.setup import get_embedding_model


def test_get_embedding_model_sentence_transformers():
    # Test case for sentence-transformers
    model = get_embedding_model("sentence-transformers", model_name="all-MiniLM-L6-v2")
    assert isinstance(model, embeddings.SentenceTransformerEmbeddings)


# def test_get_embedding_model_openai():
#     # Test case for OpenAI
#     model = get_embedding_model("openai", model="text-embedding-ada-002")
#     assert isinstance(model, embeddings.OpenAIEmbeddings)


def test_get_embedding_model_unsupported_type():
    # Test case for unsupported model type
    with pytest.raises(ValueError) as e_info:
        model = get_embedding_model("unsupported_model_type")
    assert str(e_info.value) == "Model type unsupported_model_type is not supported."


if __name__ == "__main__":
    pytest.main(["-vv", "test_get_embedding_model.py"])

"""Contains the functionality to perform extractive question answering."""
import functools
from typing import Any, Tuple

from transformers import (AutoModelForQuestionAnswering,
                          AutoTokenizer,
                          pipeline)


EXTRACTIVE_MODEL_NAMES = [
    "deepset/roberta-base-squad2",
]


@functools.lru_cache(maxsize=1)
def _load_extractive_model(model_name: str = "deepset/roberta-base-squad2"
                           ) -> Tuple[Any, Any]:
    """Loads the extractive question answering model.

    Args:
        model_name (str, optional): The model name. Defaults to
            "deepset/roberta-base-squad2".

    Returns:
        AutoModelForQuestionAnswering, AutoTokenizer: The model and tokenizer.
    """
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer


def get_extractive_answer(question: str,
                          context: str,
                          model_name: str = "deepset/roberta-base-squad2",
                          ) -> str:
    """Returns the answer to a question using extractive question answering.

    Args:
        question (str): The question.
        context (str): The context.
        model_name (str, optional): The model name. Defaults to
            "deepset/roberta-base-squad2".

    Returns:
        A dictionary with the 'answer' as a string, the 'score' as a float and
        the 'start' and 'end' as integers.
    """
    model, tokenizer = _load_extractive_model(model_name)
    qa_input = {
        'question': question,
        'context': context
    }
    nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)
    res = nlp(qa_input)
    return res

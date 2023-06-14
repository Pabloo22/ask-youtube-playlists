"""Contains the functionality to perform extractive question answering.

from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

model_name = "deepset/roberta-base-squad2"

# a) Get predictions
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
QA_input = {
    'question': 'Why is model conversion important?',
    'context': 'The option to convert models between FARM and transformers
    gives freedom to the user and let people easily switch between frameworks.'
}
res = nlp(QA_input)

# b) Load model & tokenizer
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
"""
import functools
from typing import Any, Tuple

from transformers import (AutoModelForQuestionAnswering,
                          AutoTokenizer,
                          pipeline)


@functools.lru_cache(maxsize=1)
def load_extractive_model(model_name: str = "deepset/roberta-base-squad2"
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
    model, tokenizer = load_extractive_model(model_name)
    qa_input = {
        'question': question,
        'context': context
    }
    nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)
    res = nlp(qa_input)
    return res

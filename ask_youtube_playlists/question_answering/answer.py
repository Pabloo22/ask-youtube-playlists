"""Contains the functionality to answer a question given a list of
documents."""
from dataclasses import dataclass
from typing import List

import langchain
from langchain import llms
from langchain.schema import Document


@dataclass
class LLMSpec:
    """Class to store the information of a language model.

    Attributes:
        name (str): The name of the language model.
        model_type (str): The class or method used to load the language model.
    """
    name: str
    model_type: str
    max_tokens: int


GENERATIVE_MODELS = [
    # LLMSpec("bloom-1b7", "huggingface_pipeline"),
    LLMSpec("gpt-3.5-turbo", "openai", max_tokens=4096),
    LLMSpec("gpt-3.5-turbo-16k", "openai", max_tokens=16384),
    LLMSpec("gpt-4", "openai", max_tokens=32768),
]


def get_model_spec(model_name: str) -> LLMSpec:
    """Returns the language model specification.

    Args:
        model_name (str): The name of the language model.

    Returns:
        LLMSpec: The language model specification.

    Raises:
        ValueError: If the language model is not available.
    """
    for model_spec in GENERATIVE_MODELS:
        if model_spec.name == model_name:
            return model_spec

    raise ValueError(f"Model '{model_name}' not available. Available "
                     f"models are: {GENERATIVE_MODELS}")


def load_model(model_spec: LLMSpec,
               temperature: float = 0.7,
               max_length: int = 128,
               ) -> llms.base.BaseLLM:
    """Loads the language model.

    Args:
        model_spec (LLMSpec): The language model specification.
        temperature (float, optional): The temperature used to generate the
            answer. The higher the temperature, the more "creative" the answer
            will be. Defaults to 0.7.
        max_length (int, optional): The maximum length of the generated answer.
            Defaults to 128.

    Returns:
        llms.base.BaseLLM: The language model.
    """

    # if model_spec.model_type == "huggingface_pipeline":
    #     return llms.HuggingFacePipeline.from_model_id(
    #         model_spec.name,
    #         task="text-generation",
    #         model_kwargs={"temperature": temperature,
    #                       "max_length": max_length}
    #     )
    if model_spec.model_type == "openai_api":
        pass


def _get_generative_prompt_template(retrieved_documents: List[Document],
                                    ) -> langchain.PromptTemplate:
    """Returns the template used to generate the answer.

    Returns:
        langchain.PromptTemplate: The template used to generate the answer.
    """
    template_text = ""
    for document in reversed(retrieved_documents):
        template_text += f"{document.page_content}\n\n"

    template_text += "Question: {question}\n\n"
    template_text += "Answer:"

    template = langchain.PromptTemplate(template=template_text,
                                        input_variables=["question"])

    return template


def get_generative_answer(question: str,
                          relevant_documents: List[Document],
                          model: llms.base.BaseLLM) -> str:
    """Returns the answer to the question as a string.

    Args:
        question (str): The question asked by the user.
        relevant_documents (List[Document]): The list of relevant documents.
        model (llms.base.BaseLLM): The language model used to generate the
            answer.

    Returns:
        str: The answer to the question.
    """

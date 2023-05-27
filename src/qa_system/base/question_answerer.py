import abc

from qa_system.data import Episode


class QuestionAnswerer(abc.ABC):
    """Base class for Question Answering component of the application."""

    @abc.abstractmethod
    def answer(self, question: str, context: Episode) -> str:
        """Answers a question based on a context.

        This is an abstract method that should be implemented by all subclasses. It takes a user's question and a
        context and returns the answer to the question based on the context.

        Args:
            question (str): The user's question.
            context (Episode): The context for the question.

        Returns:
            str: The answer to the question.
        """

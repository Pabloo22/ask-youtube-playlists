"""Facade class that uses the Question Answering system"""
import pathlib


class QuestionAnswerer:

    def __init__(self,
                 data_path: pathlib.Path):
        self.data_path = data_path

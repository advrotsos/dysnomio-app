from . import dictionary as dct
from .exceptions import WordNotFound, InvalidGuess
from .gpt import GPTHelper


class Guess:
    def __init__(self, word) -> None:
        self.word = word
        self.length = len(self.word)
        try:
            self.prep()
        except WordNotFound:
            raise InvalidGuess

    def prep(self) -> None:
        self.retrieve_part_of_speech()
        self.call_openai()

    def retrieve_part_of_speech(self) -> None:
        self.part_of_speech = dct.DictionaryAPI(self.word).call_and_parse()[
            "part_of_speech"
        ]

    def call_openai(self) -> None:
        self.complexity = GPTHelper().call_api_for_complexity(self.word)

    def __len__(self):
        return len(self.word)

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

        pos_map = {
            "noun": "n.",
            "verb": "v.",
            "pronoun": "pro.",
            "adjective": "adj.",
            "adverb": "adv.",
            "conjunction": "conj.",
            "interjection": "interj.",
        }

        part_of_speech = dct.DictionaryAPI(self.word).call_and_parse()["part_of_speech"]

        try:
            len(part_of_speech)
            self.part_of_speech = [pos_map.get(x.lower(), x) for x in part_of_speech]
        except:
            self.part_of_speech = pos_map.get(part_of_speech.lower(), part_of_speech)

    def call_openai(self) -> None:
        self.complexity = GPTHelper().call_api_for_complexity(self.word)

    def __len__(self):
        return len(self.word)

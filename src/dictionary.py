import os
import time
import json
import requests
import pandas as pd
import numpy as np
import data.words as words
from src.exceptions import WordNotFound


class DictionaryAPI:
    """Dictionary API call to return word characteristics. """

    def __init__(self, word) -> None:
        self.url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word

    def make_api_call(self, url) -> json:
        # NOTE: I can probably design this section a lot better
        # Make this a TODO.
        response = requests.get(self.url).json()
        if self.is_word(response):
            return response
        else:
            raise WordNotFound

    def is_word(self, api_response) -> bool:
        # NOTE: this is kinda silly, I can definitely make this better
        try:
            api_response["title"]
            return False
        except TypeError as e:
            return True

    def parse_api_response(self, data) -> pd.DataFrame:
        self.word = []
        self.part_of_speech = []
        self.definition = []
        for i in range(len(data[0]["meanings"])):
            self.word.append(data[0]["word"])
            self.part_of_speech.append(data[0]["meanings"][i]["partOfSpeech"])
            # NOTE: For now, only grab the first definition per PoS
            self.definition.append(
                data[0]["meanings"][i]["definitions"][0]["definition"]
            )
        return dict(
            word=self.word,
            part_of_speech=self.part_of_speech,
            definition=self.definition,
        )

    def call_and_parse(self) -> pd.DataFrame:
        self.json_data = self.make_api_call(self.url)
        self.output = self.parse_api_response(self.json_data)
        return self.output

import os
import time
import json
import requests
from typing import Dict, List, Any
import pandas as pd
import numpy as np
import data.words as words
from src.exceptions import WordNotFound


class DictionaryAPI:
    """Dictionary API call to return word characteristics."""

    BASE_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

    def __init__(self, word: str) -> None:
        self.word = word
        self.url = self.BASE_URL + word

    def make_api_call(self) -> List[Dict[str, Any]]:
        response = requests.get(self.url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        
        if isinstance(data, dict) and "title" in data:
            raise WordNotFound(f"Word '{self.word}' not found in the dictionary.")
        
        return data

    def parse_api_response(self, data: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        parsed_data = {
            "word": [],
            "part_of_speech": [],
            "definition": []
        }
        
        for entry in data:
            word = entry["word"]
            for meaning in entry["meanings"]:
                parsed_data["word"].append(word)
                parsed_data["part_of_speech"].append(meaning["partOfSpeech"])
                parsed_data["definition"].append(meaning["definitions"][0]["definition"])
        
        return parsed_data

    def call_and_parse(self) -> pd.DataFrame:
        try:
            json_data = self.make_api_call()
            parsed_data = self.parse_api_response(json_data)
            return pd.DataFrame(parsed_data)
        except requests.RequestException as e:
            raise RuntimeError(f"API request failed: {str(e)}") from e
import os
import random
from typing import Union, List
from . import dictionary as dct
import data.words as words
from .exceptions import WordNotFound, InvalidGuess, RepeatGuess
from .gpt import GPTHelper
from .guess import Guess


class Thesaurdle:
    def __init__(self, difficulty: str = "hard", rounds: int = 5) -> None:
        self.gameover = False
        self.rounds = rounds
        self.difficulty = difficulty
        self.lives = rounds
        self.guesses = []
        self.answer = self.retrieve_answer(difficulty=self.difficulty)
        self.answer.complexity = GPTHelper().call_api_for_complexity(self.answer.word)
        self.formatted_answer = (
            self.answer.word.capitalize()
            + " "
            + f"({self.answer.part_of_speech.capitalize()}): "
            + self.answer.definition
        )
        # self.initial_hint(self.answer.word)
        self.guess_hint = ""  # stop-gap to avoid weird interaction in flask app

    def play(self) -> None:
        """For every round, submit a guess. Break the loop if you win, else `lose`."""
        print(self.initial_hint(self.answer.word))
        while self.lives > 0:
            if self.gameover:
                break
            elif self.lives == 0:
                break
            self.guess()
        # This will always trigger win or lose, so keep the function minimal, like showing the answer.
        # Essetially the stop condition. Might want to do this differently.
        self.lose()

    def guess(self, word) -> None:
        guess = Guess(word)
        self.current_guess = guess.word
        self.process_guess(guess)

        if self.gameover or self.lives == 0:
            self.lose()

        if guess.word == self.answer.word:
            self.win()
        else:
            self.lives -= 1

    def win(self) -> None:
        print("\nCongrats! You win.\n")
        self.gameover = True

    def lose(self) -> None:
        print(self.answer, "\n")
        self.gameover = True

    def process_guess(self, guess: Guess) -> None:
        feedback = ["\n"]
        self.judge_part_of_speech(guess, feedback)
        self.judge_len(guess, feedback)
        self.judge_complexity(guess, feedback)
        self.judge_definition_similarity(guess, feedback)
        self.hint(guess, feedback)

    def judge_part_of_speech(self, guess: Guess, feedback: str) -> None:
        if self.answer.part_of_speech in guess.part_of_speech:
            self.guess_part_of_speech = f"{self.answer.part_of_speech}"
        else:
            self.guess_part_of_speech = "{}".format(
                ", ".join([x for x in set(guess.part_of_speech)])
            )

    def judge_len(self, guess: Guess, feedback: str) -> None:
        lendiff = guess.length - self.answer.length
        self.lendiff = abs(lendiff)
        self.guess_word_len = guess.length

    def judge_complexity(self, guess: Guess, feedback: str) -> None:
        self.compdiff = abs(int(guess.complexity) - int(self.answer.complexity))
        self.guess_complexity = f"{guess.complexity} / 5"

    def judge_definition_similarity(self, guess: Guess, feedback: str) -> None:
        sim = GPTHelper().call_api_for_similarity(guess.word, self.answer.word)
        self.guess_sim_num = sim
        self.guess_sim = f"{sim} / 5"

    def hint(self, guess: Guess, feedback: str) -> None:
        self.guess_hint = GPTHelper().call_api_for_hints(guess.word, self.answer.word)

    def initial_hint(self, answer: str) -> str:
        return GPTHelper().call_api_for_initial_hint(answer)

    def retrieve_answer(self, difficulty: str) -> str:
        # Format this better please
        return (
            words.word_list[words.word_list.difficulty == difficulty]
            .reset_index(drop=True)
            .loc[
                random.choice(
                    range(
                        len(
                            words.word_list[
                                words.word_list.difficulty == difficulty
                            ].reset_index(drop=True)
                        )
                    )
                )
            ]
        )

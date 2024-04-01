import os
import random
from typing import Union, List
from . import dictionary as dct
import data.words as words
from .exceptions import WordNotFound, InvalidGuess
from .gpt import GPTHelper
from .guess import Guess


class Thesaurdle:
    def __init__(self, rounds: int = 5) -> None:
        self.gameover = False
        self.rounds = rounds
        self.lives = rounds
        self.guesses = []
        self.answer = self.retrieve_answer()
        self.answer.complexity = GPTHelper().call_api_for_complexity(self.answer.word)

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
        self.guesses.append(guess)
        if self.gameover:
            self.lose()
        if self.lives == 0:
            self.lose()
        if guess.word == self.answer.word:
            self.win()
        else:
            self.process_guess(guess)
            self.lives -= 1

    def win(self) -> None:
        print("\nCongrats! You win.\n")
        self.gameover = True

    def lose(self) -> None:
        print(self.answer, "\n")
        self.gameover = True

    def prompt_for_guess(self) -> str:
        """Prompt user for guess. If WordNotFound, keep prompting until guess is valid"""
        valid_guess = False
        while not valid_guess:
            try:
                guess = (
                    str(input(f"What is your guess? Turns remaining: {self.lives} "))
                    .strip()
                    .lower()
                )
                g = Guess(guess)
                valid_guess = True
            except InvalidGuess:
                print("Word not found. Try again.")
        return g

    def process_guess(self, guess: Guess) -> None:
        feedback = ["\n"]
        self.judge_part_of_speech(guess, feedback)
        self.judge_len(guess, feedback)
        self.judge_complexity(guess, feedback)
        self.judge_definition_similarity(guess, feedback)
        self.hint(guess, feedback)
        print("".join(feedback))

    def judge_part_of_speech(self, guess: Guess, feedback: str) -> None:
        if self.answer.part_of_speech in guess.part_of_speech:
            feedback.append("Part of Speech: Correct\n")
            self.guess_part_of_speech = "Part of Speech: Correct"
        else:
            feedback.append("Part of Speech: Incorrect\n")
            self.guess_part_of_speech = "Part of Speech: Incorrect"

    def judge_len(self, guess: Guess, feedback: str) -> None:
        lendiff = guess.length - self.answer.length
        if lendiff == 0:
            feedback.append(f"Word Length: {guess.length}\n")
            self.guess_word_len = f"Word Length: {guess.length}"
        if lendiff < 0:
            feedback.append(f"Word Length: + {abs(lendiff)}\n")
            self.guess_word_len = f"Word Length: + {abs(lendiff)}"
        if lendiff > 0:
            feedback.append(f"Word Length: - {abs(lendiff)}\n")
            self.guess_word_len = f"Word Length: - {abs(lendiff)}"

    def judge_complexity(self, guess: Guess, feedback: str) -> None:
        # NOTE: this is a temp solution until I add this col to word list db
        feedback.append(
            f"Guess Complexity: {guess.complexity}, Answer Complexity: {self.answer.complexity}\n"
        )
        self.guess_complexity = f"Guess Complexity: {guess.complexity}, Answer Complexity: {self.answer.complexity}"

    def judge_definition_similarity(self, guess: Guess, feedback: str) -> None:
        sim = GPTHelper().call_api_for_similarity(guess.word, self.answer.word)
        feedback.append(f"Similarity: {sim}\n")
        self.guess_sim = f"Similarity: {sim}"

    def hint(self, guess: Guess, feedback: str) -> None:
        # feedback.append(
        #     f"\n{GPTHelper().call_api_for_hints(guess.word, self.answer.word)}\n"
        # )

        self.guess_hint = GPTHelper().call_api_for_hints(guess.word, self.answer.word)

    def initial_hint(self, answer: str) -> str:
        return GPTHelper().call_api_for_initial_hint(answer)

    def retrieve_answer(self) -> str:
        return words.word_list.loc[random.choice(range(len(words.word_list)))]

import random
from typing import List
from openai import OpenAI
from data.hint_prompts import hint_prompts
from .models import roles


class GPTHelper:
    def __init__(self) -> None:
        self.client = OpenAI()
        self.model = "gpt-3.5-turbo"

    def call_api_for_complexity(self, word: str) -> None:
        self.complexity_model_user_role = f"On a scale of 1-5, how would you rate the complexity of the word {word}? \
                                            Be strict - give simple or common words low scores. \
                                            Return the response as a single integer number. "

        self.complexity_model = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are amazing! :) "},
                {"role": "user", "content": self.complexity_model_user_role},
            ],
        )

        try:
            return int(self.complexity_model.choices[0].message.content.strip("."))
        except ValueError as e:
            # if gpt returns sentence, strip the period and grab the last char
            # with should be the number...
            return [x for x in self.complexity_model.choices[0].message.content if x.isdigit()][0]

    def call_api_for_similarity(self, guess: str, answer: str) -> str:
        self.similarity_model_user_role = f"On a scale of 1-5, how similar are the definitions of {guess} and {answer}. \
                                            Return the response as a single integer number. "

        self.similarity_model = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": self.similarity_model_user_role}],
        )

        return self.similarity_model.choices[0].message.content.strip(".")

    def call_api_for_hints(self, guess: str, answer: str) -> str:
        self.hint_model_system_role = roles.hint_model_system_roles.get("v3")
        self.hint_model_user_role = roles.hint_model_user_roles.get("v2").format(
            guess=guess, answer=answer
        )
        self.hint_model = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.hint_model_system_role},
                {"role": "user", "content": self.hint_model_user_role},
            ],
        )

        return self.hint_model.choices[0].message.content

    def call_api_for_initial_hint(self, answer) -> str:
        prompt = self.retrieve_initial_hint_prompt()
        self.initial_hint_model_system_role = roles.initial_hint_model_system_roles.get(
            "v1"
        )
        self.initial_hint_model_user_role = roles.initial_hint_model_user_roles.get(
            "v1"
        ).format(prompt=prompt, answer=answer)
        self.initial_hint_model = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.initial_hint_model_system_role},
                {"role": "user", "content": self.initial_hint_model_user_role},
            ],
        )

        return "\n" + self.initial_hint_model.choices[0].message.content + "\n"

    def retrieve_initial_hint_prompt(self) -> str:
        return hint_prompts[random.choice(range(len(hint_prompts)))]

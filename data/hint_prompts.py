import random

actors = [
    "Tom Cruise",
    "Leonardo DiCaprio",
    "Robert DeNiro",
    "Paul Dano",
    "Ethan Hawke",
]

hint_prompts = [
    "write a haiku",
    "write a brief sonnet",
    "create a fake rap verse",
    "create a fake country song verse",
    "write a short synopsis of fake movie starring {}. Give the movie a fake name, and pretend it's real.".format(
        actors[random.choice(range(len(actors)))]
    ),
    "introduce a fight between two boxers in an old-timey prose",
    "write a short poem",
    "make a pitch to the judges on Shark Tank",
]

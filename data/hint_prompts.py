import random

actors = ["Tom Cruise", "Leonardo DiCaprio", "Robert DeNiro"]

hint_prompts = [
    "write a haiku",
    "write a brief sonnet",
    "create a fake rap verse",
    "create a fake country song verse",
    "write a short synopsis of fake movie starring {}".format(
        actors[random.choice(range(len(actors)))]
    ),
    # "describe a delicious meal prepared by a fine dining chef. Describe the food.",  # this seems to be producing odd results
    "introduce a fight between two boxers in an old-timey prose",
    "describe a fake half-time show performance at the Super Bowl",
]

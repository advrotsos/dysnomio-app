import random

actors = [
    "Tom Cruise",
    "Leonardo DiCaprio",
    "Robert DeNiro",
    "Paul Dano",
    "Ethan Hawke",
]

authors = [
    "Mark Twain",
    "Edgar Allen Poe",
    "Ernest Hemmingway",
    "William Faulkner",
    "Cormac McCarthy",
    "William Shakespeare",
    "Stephen King",
]

hint_prompts = [
    "write a haiku",
    "write a brief sonnet",
    "create a fake rap verse. go right into the verse, pretend you are singing it.",
    "create a fake country song verse",
    "write a short synopsis of fake movie starring {}. Give the movie a fake name, and pretend it's real.".format(
        actors[random.choice(range(len(actors)))]
    ),
    "introduce a fight between two boxers in an old-timey prose. keep the response somewhat brief. ",
    "write a short poem or excerpt in the style of {}".format(
        authors[random.choice(range(len(authors)))]
    ),
    "make a pitch to the judges on Shark Tank",
]

from flask import Flask, redirect, url_for, render_template, request
from src.game import Thesaurdle

app = Flask(__name__)
game = Thesaurdle()
lives_remaining = 5
guess_count = 0
answer = game.answer

date = "Tuesday, April 2 2024"


@app.route("/")
def landing():
    return render_template("landing.html", date=date)


@app.route("/home")  # change back to "/" ?
def home():
    return render_template("index.html", lives=lives_remaining, guess_count=guess_count)


@app.route("/guess", methods=["POST", "GET"])
def process_guess():
    global lives_remaining, guess_count, answer

    if request.method == "POST":
        g = request.form["guess"]
        game.guess(g)
        # if game.current_guess == answer:
        #     render_template("/win.html")
        guess_count += 1
        lives_remaining -= 1
        if lives_remaining < 0:  # lose on the sixth guess
            return render_template("/lose.html")

    return render_template(
        "index.html",
        guess_hint=game.guess_hint,
        guess_part_of_speech=game.guess_part_of_speech,
        answer_part_of_speech=game.answer.part_of_speech,
        guess_word_len=game.guess_word_len,
        guess_complexity=game.guess_complexity,
        guess_sim=game.guess_sim,
        lives=int(lives_remaining),
        guess_count=guess_count,
    )


@app.route("/win.html")
def win():
    return render_template("win.html")


@app.route("/lose.html")
def lose():
    return render_template("lose.html")


if __name__ == "__main__":
    app.run(debug=True)

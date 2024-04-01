from flask import Flask, redirect, url_for, render_template, request
from src.game import Thesaurdle

app = Flask(__name__)
game = Thesaurdle()
guess_no = 0


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/", methods=["POST", "GET"])
def process_guess():
    if request.method == "POST":
        g = request.form["guess"]
    game.guess(g)
    return render_template(
        "index.html",
        guess_hint=game.guess_hint,
        guess_part_of_speech=game.guess_part_of_speech,
        answer_part_of_speech=game.answer.part_of_speech,
        guess_word_len=game.guess_word_len,
        guess_complexity=game.guess_complexity,
        guess_sim=game.guess_sim,
        game_guesses=len(game.guesses),
    )


@app.route("/win.html")
def win():
    return render_template("win.html")


@app.route("/lose.html")
def lose():
    return render_template("lose.html")


if __name__ == "__main__":
    app.run(debug=True)

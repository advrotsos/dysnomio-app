from datetime import date
from flask import Flask, redirect, url_for, render_template, request
from src.game import Thesaurdle

app = Flask(__name__)
todaydate = date.today().strftime("%A, %B %-d %Y")


@app.route("/")
def landing():
    global game, lives_remaining, guess_count, answer, answer_complexity
    game = Thesaurdle()
    lives_remaining = 5
    guess_count = 0
    answer = game.answer.word
    answer_complexity = game.answer.complexity
    print(answer)
    return render_template("landing.html", date=todaydate)


@app.route("/restart", methods=["GET"])
def restart():
    return redirect(url_for("landing"))


@app.route("/home")  # change back to "/" ?
def home():
    return render_template(
        "index.html",
        lives=lives_remaining,
        guess_count=guess_count,
        init_hint=game.init_hint,
        date=todaydate,
    )


@app.route("/guess", methods=["POST", "GET"])
def process_guess():
    global lives_remaining, guess_count, answer
    if request.method == "POST":
        g = request.form["guess"]
        try:
            game.guess(g)
        except Exception as e:
            invalid_guess = True
            if guess_count == 0:
                return render_template(
                    "index.html",
                    invalid_guess=invalid_guess,
                    lives=lives_remaining,
                    guess_count=guess_count,
                )
            else:
                return render_template(
                    "index.html",
                    guess_hint=game.guess_hint,
                    init_hint=game.init_hint,
                    guess_part_of_speech=game.guess_part_of_speech,
                    answer_part_of_speech=game.answer.part_of_speech,
                    lendiff=game.lendiff,
                    answer_word_len=game.answer.length,
                    guess_word_len=game.guess_word_len,
                    guess_complexity=game.guess_complexity,
                    compdiff=game.compdiff,
                    answer_complexity=answer_complexity,
                    guess_sim=game.guess_sim,
                    lives=int(lives_remaining),
                    guess_count=guess_count,
                    date=todaydate,
                    invalid_guess=invalid_guess,
                )

        # if game.current_guess in game.guesses:
        #     return render_template("index.html")

        if game.current_guess == answer:
            return render_template("/win.html")
        guess_count += 1
        lives_remaining -= 1
        if lives_remaining < 0:  # lose on the sixth guess
            return render_template("/lose.html")

    return render_template(
        "index.html",
        guess_hint=game.guess_hint,
        init_hint=game.init_hint,
        guess_part_of_speech=game.guess_part_of_speech,
        answer_part_of_speech=game.answer.part_of_speech,
        lendiff=game.lendiff,
        answer_word_len=game.answer.length,
        guess_word_len=game.guess_word_len,
        guess_complexity=game.guess_complexity,
        compdiff=game.compdiff,
        answer_complexity=answer_complexity,
        guess_sim=game.guess_sim,
        lives=int(lives_remaining),
        guess_count=guess_count,
        date=todaydate,
    )


@app.route("/win.html")
def win():
    return render_template("win.html", date=todaydate)


@app.route("/lose.html")
def lose():
    return render_template("lose.html", date=todaydate)


if __name__ == "__main__":
    app.run(debug=True)

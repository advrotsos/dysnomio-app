from datetime import date
from flask import Flask, redirect, url_for, render_template, request
from src.game import Thesaurdle
from src.exceptions import InvalidGuess, RepeatGuess


app = Flask(__name__)
todaydate = date.today().strftime("%A, %B %-d %Y")
difficulty = "Hard"


@app.route("/")
def landing():
    global lives_remaining, guess_count
    lives_remaining = 5
    guess_count = 0
    return render_template("landing.html", date=todaydate)


@app.route("/select", methods=["POST"])
def select():
    global difficulty, game
    if request.method == "POST":
        difficulty = request.form["difficulty"]
        game = Thesaurdle(difficulty=difficulty)
        return render_template(
            "index.html",
            lives=lives_remaining,
            guess_count=guess_count,
            init_hint=game.init_hint,
            date=todaydate,
            difficulty=difficulty,
        )


@app.route("/restart", methods=["GET"])
def restart():
    return redirect(url_for("landing"))


@app.route("/home")
def home():
    global game, lives_remaining, guess_count, difficulty
    return render_template(
        "index.html",
        lives=lives_remaining,
        guess_count=guess_count,
        init_hint=game.init_hint,
        date=todaydate,
        difficulty=difficulty,
    )


@app.route("/guess", methods=["POST", "GET"])
def process_guess():
    global lives_remaining, guess_count, answer, difficulty, game, answer_complexity
    answer = game.answer.word
    answer_complexity = game.answer.complexity
    print(difficulty, answer)
    invalid_guess = False
    if request.method == "POST":
        g = request.form["guess"]
        try:
            game.guess(g)
        except InvalidGuess:
            invalid_guess = True
            if guess_count == 0:
                return render_template(
                    "index.html",
                    invalid_guess=invalid_guess,
                    lives=lives_remaining,
                    guess_count=guess_count,
                    init_hint=game.init_hint,
                    date=todaydate,
                    difficulty=difficulty,
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
                    guess_sim_num=int(game.guess_sim_num.strip(".")),
                    lives=int(lives_remaining),
                    guess_count=guess_count,
                    date=todaydate,
                    invalid_guess=invalid_guess,
                    difficulty=difficulty,
                )
        except RepeatGuess:
            repeat_guess = True
            invalid_guess = False
            return render_template(
                "index.html",
                repeat_guess=repeat_guess,
                invalid_guess=invalid_guess,  # Pass invalid_guess to the template
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
                guess_sim_num=int(game.guess_sim_num),
                lives=int(lives_remaining),
                guess_count=guess_count,
                date=todaydate,
                difficulty=difficulty,
            )

        if game.current_guess == answer:
            guess_count += 1
            return render_template(
                "/win.html",
                date=todaydate,
                formatted_answer=game.formatted_answer,
                guess_count=guess_count,
                difficulty=difficulty,
            )

        guess_count += 1
        lives_remaining -= 1
        if lives_remaining < 0:  # lose on the sixth guess
            return render_template(
                "/lose.html",
                date=todaydate,
                formatted_answer=game.formatted_answer,
                guess_count=guess_count,
                difficulty=difficulty,
            )

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
        guess_sim_num=int(game.guess_sim_num),
        lives=int(lives_remaining),
        guess_count=guess_count,
        date=todaydate,
        invalid_guess=invalid_guess,
        difficulty=difficulty,
    )


@app.route("/win.html")
def win():
    return render_template("win.html", date=todaydate, difficulty=difficulty)


@app.route("/lose.html")
def lose():
    global difficulty
    return render_template("lose.html", date=todaydate, difficulty=difficulty)


if __name__ == "__main__":
    app.run(debug=True)

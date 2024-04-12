from datetime import date
from flask import Flask, redirect, url_for, render_template, request, session
from src.game import Thesaurdle
from src.exceptions import InvalidGuess, RepeatGuess


app = Flask(__name__)
app.secret_key = "KEY123ABCMUADDIB"
todaydate = date.today().strftime("%A, %B %-d %Y")
difficulty: str = "Hard"  # placeholder in case something fails
lives: int = 5


@app.route("/")
def landing():
    session.clear()
    return render_template("landing.html", date=todaydate)


@app.route("/select", methods=["POST"])
def select():
    global game
    if request.method == "POST":
        difficulty = request.form["difficulty"]
        game = Thesaurdle(difficulty=difficulty)
        if "game_state" not in session:
            session["game_state"] = {
                "init_hint": game.initial_hint(game.answer.word),
                "lives_remaining": int(lives),
                "guess_count": 0,
                "answer": game.answer.word,
                "answer_complexity": int(game.answer.complexity),
                "answer_part_of_speech": game.answer.part_of_speech,
                "answer_len": int(game.answer.length),
                "formatted_answer": game.formatted_answer,
                "difficulty": difficulty,
                "guesses": [],
                "hints": [],
                "guess_feedback": {},
            }
        return render_template(
            "index.html",
            lives=session["game_state"]["lives_remaining"],
            guess_count=session["game_state"]["guess_count"],
            init_hint=session["game_state"]["init_hint"],
            date=todaydate,
            difficulty=session["game_state"]["difficulty"],
        )


@app.route("/restart", methods=["GET"])
def restart():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/guess", methods=["POST", "GET"])
def process_guess():
    if "lives_remaining" not in session:
        session["lives_remaining"] = 5
    if "guess_count" not in session:
        session["guess_count"] = 0
    print(session["game_state"]["difficulty"], session["game_state"]["answer"])
    invalid_guess = False
    if request.method == "POST":
        g = request.form["guess"]
        try:
            game = Thesaurdle(difficulty=session["game_state"]["difficulty"])
            game.init_hint = session["game_state"]["init_hint"]
            game.answer.word = session["game_state"]["answer"]
            game.answer.complexity = session["game_state"]["answer_complexity"]
            guess_feedback = []
            game.guess(g)
            if game.current_guess in session["game_state"]["guesses"]:
                raise RepeatGuess
            session["game_state"]["guesses"].append(game.current_guess)
            session["game_state"]["last_guess"] = game.current_guess
            session["game_state"]["hints"].append(game.guess_hint)
            session["game_state"]["last_guess_hint"] = game.guess_hint
            session["game_state"][
                "last_guess_part_of_speech"
            ] = game.guess_part_of_speech
            # assess part of speech
            if (
                session["game_state"]["answer_part_of_speech"]
                in session["game_state"]["last_guess_part_of_speech"]
            ):
                print("pos: 2")
                guess_feedback.append(2)
            else:
                print("pos: 0")
                guess_feedback.append(0)
            session["game_state"]["last_guess_lendiff"] = int(game.lendiff)
            # assess lendiff
            if session["game_state"]["last_guess_lendiff"] == 0:
                print("last_guess_lendiff: 2")
                guess_feedback.append(2)
            elif session["game_state"]["last_guess_lendiff"] in [1, 2]:
                print("last_guess_lendiff: 1")
                guess_feedback.append(1)
            else:
                print("last_guess_lendiff: 0")
                guess_feedback.append(0)
            session["game_state"]["last_guess_word_len"] = int(game.guess_word_len)
            session["game_state"]["last_guess_complexity"] = game.guess_complexity
            session["game_state"]["last_guess_compdiff"] = int(game.compdiff)
            # assess compdiff
            if int(session["game_state"]["last_guess_compdiff"]) == 0:
                guess_feedback.append(2)
            elif int(session["game_state"]["last_guess_compdiff"]) in [1, 2]:
                guess_feedback.append(1)
            else:
                guess_feedback.append(0)
            session["game_state"]["last_guess_sim"] = game.guess_sim
            session["game_state"]["last_guess_sim_num"] = int(
                game.guess_sim_num.strip(".")
            )
            # assess sim num
            if session["game_state"]["last_guess_sim_num"] == 5:
                guess_feedback.append(2)
            elif session["game_state"]["last_guess_sim_num"] == 4:
                guess_feedback.append(1)
            else:
                print("last_guess_sim_num: 0")
            session["game_state"]["guess_feedback"][
                str(session["guess_count"])
            ] = guess_feedback
        except InvalidGuess:
            invalid_guess = True
            if session["guess_count"] == 0:
                return render_template(
                    "index.html",
                    invalid_guess=invalid_guess,
                    lives=session["lives_remaining"],
                    guess_count=session["guess_count"],
                    init_hint=session["game_state"]["init_hint"],
                    date=todaydate,
                    difficulty=session["game_state"]["difficulty"],
                )
            else:
                return render_template(
                    "index.html",
                    guess_hint=session["game_state"]["last_guess_hint"],
                    init_hint=session["game_state"]["init_hint"],
                    guess_part_of_speech=session["game_state"][
                        "last_guess_part_of_speech"
                    ],
                    answer_part_of_speech=session["game_state"][
                        "answer_part_of_speech"
                    ],
                    lendiff=session["game_state"]["last_guess_word_len"],
                    answer_word_len=session["game_state"]["answer_len"],
                    guess_word_len=session["game_state"]["last_guess_word_len"],
                    guess_complexity=session["game_state"]["last_guess_complexity"],
                    compdiff=session["game_state"]["last_guess_compdiff"],
                    answer_complexity=session["game_state"]["answer_complexity"],
                    guess_sim=session["game_state"]["last_guess_sim"],
                    guess_sim_num=int(session["game_state"]["last_guess_sim_num"]),
                    lives=int(session["lives_remaining"]),
                    guess_count=session["guess_count"],
                    date=todaydate,
                    invalid_guess=invalid_guess,
                    difficulty=session["game_state"]["difficulty"],
                )
        except RepeatGuess:
            repeat_guess = True
            invalid_guess = False
            return render_template(
                "index.html",
                repeat_guess=repeat_guess,
                invalid_guess=invalid_guess,  # Pass invalid_guess to the template
                guess_hint=session["game_state"]["last_guess_hint"],
                init_hint=session["game_state"]["init_hint"],
                guess_part_of_speech=session["game_state"]["last_guess_part_of_speech"],
                answer_part_of_speech=session["game_state"]["answer_part_of_speech"],
                lendiff=session["game_state"]["last_guess_lendiff"],
                answer_word_len=session["game_state"]["answer_len"],
                guess_word_len=session["game_state"]["last_guess_word_len"],
                guess_complexity=session["game_state"]["last_guess_complexity"],
                compdiff=session["game_state"]["last_guess_compdiff"],
                answer_complexity=session["game_state"]["answer_complexity"],
                guess_sim=session["game_state"]["last_guess_sim"],
                guess_sim_num=int(session["game_state"]["last_guess_sim_num"]),
                lives=int(session["lives_remaining"]),
                guess_count=session["guess_count"],
                date=todaydate,
                difficulty=session["game_state"]["difficulty"],
            )

        if session["game_state"]["last_guess"] == session["game_state"]["answer"]:
            print("good")
            session["guess_count"] += 1
            return render_template(
                "/win.html",
                date=todaydate,
                formatted_answer=session["game_state"]["formatted_answer"],
                guess_count=session["guess_count"],
                difficulty=session["game_state"]["difficulty"],
            )

        if int(session["guess_count"]) < 5:
            session["guess_count"] += 1
        else:
            session["guess_count"] = 5
        session["lives_remaining"] -= 1
        if int(session["lives_remaining"]) < 0:  # lose on the sixth guess
            return render_template(
                "/lose.html",
                date=todaydate,
                formatted_answer=session["game_state"]["formatted_answer"],
                guess_count=session["guess_count"],
                difficulty=session["game_state"]["difficulty"],
            )

    return render_template(
        "index.html",
        guess_hint=session["game_state"]["last_guess_hint"],
        init_hint=session["game_state"]["init_hint"],
        guess_part_of_speech=session["game_state"]["last_guess_part_of_speech"],
        answer_part_of_speech=session["game_state"]["answer_part_of_speech"],
        lendiff=session["game_state"]["last_guess_lendiff"],
        answer_word_len=session["game_state"]["answer_len"],
        guess_word_len=session["game_state"]["last_guess_word_len"],
        guess_complexity=session["game_state"]["last_guess_complexity"],
        compdiff=session["game_state"]["last_guess_compdiff"],
        answer_complexity=session["game_state"]["answer_complexity"],
        guess_sim=session["game_state"]["last_guess_sim"],
        guess_sim_num=int(session["game_state"]["last_guess_sim_num"]),
        lives=int(session["lives_remaining"]),
        guess_count=session["guess_count"],
        date=todaydate,
        invalid_guess=invalid_guess,
        difficulty=session["game_state"]["difficulty"],
    )


@app.route("/win.html")
def win():
    return render_template(
        "win.html", date=todaydate, difficulty=session["game_state"]["difficulty"]
    )


@app.route("/lose.html")
def lose():
    global difficulty
    return render_template(
        "lose.html", date=todaydate, difficulty=session["game_state"]["difficulty"]
    )


if __name__ == "__main__":
    app.run(debug=True)

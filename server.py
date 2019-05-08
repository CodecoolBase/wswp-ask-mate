from flask import Flask, render_template, request, redirect, url_for
import connection
import data_handler



app = Flask(__name__)

@app.route('/list')
def route_list():
    questions = connection.read_data('sample_data/question.csv')
    return render_template('list.html', questions=questions, q_keys=data_handler.QUESTION_KEYS)

@app.route('/question/<question_id>')
def display_question(question_id):
    displayed_question = data_handler.get_story_by_id('sample_data/question.csv', question_id)
    displayed_answers = data_handler.get_answers_by_question_id('sample_data/answer.csv', question_id)
    return render_template('question.html', question=displayed_question, answers=displayed_answers)

@app.route('/add_question', methods=('GET', 'POST'))
def ask_question():
    if request.method == "POST":
        new_question = {}
        for key in request.form.keys():
            new_question[key] = request.form[key]
        connection.append_data('sample_data/question.csv', new_question, data_handler.QUESTION_KEYS)
        return redirect("/list")
    return render_template("add_question.html")








if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect
import data_manager

app = Flask(__name__)


@app.route('/')
def render_index():
    questions = data_manager.collect_questions()
    return render_template('index.html', questions=questions)


@app.route('/question_page/<question_id>/vote')
def vote(question_id,vote_ud):
    vote = 0
    if vote_ud == 'up':
        vote += 1
    if vote_ud == 'down':
        vote -= 1
    data_manager.update_vote_number(vote=vote, q_id=question_id)
    return redirect('/question_page/<question_id>')


@app.route('/question_page/<question_id>')
def show_question(question_id):
    question = data_manager.find_question(q_id=question_id)
    answers = data_manager.collect_answers(q_id=question_id)
    data_manager.update_view_number(q_id=question_id)
    return render_template('question_page.html', question=question, answers=answers)


@app.route('/question_page/<question_id>/edit')
def edit_question(question_id):
    result = data_manager.find_question(q_id=question_id)
    return render_template('add_question.html', result=result)


@app.route('/rewrite_question', methods=['POST'])
def rewrite_question():
    updated_question = {
        'id': request.form.get('id'),
        'submission_time': request.form.get('submission_time'),
        'view_number': request.form.get('view_number'),
        'vote_number': request.form.get('vote_number'),
        'title': request.form.get('title'),
        'message': request.form.get('message'),
        'image': request.form.get('image')
    }
    data_manager.update_question(datas=updated_question)
    return redirect('/')


@app.route('/question_page/<question_id>/new-answer', methods=['GET','POST'])
def post_an_answer(question_id):
    result = []
    message = ""
    if request.method=='POST':
        new_answer = create_answer(question_id, request.form['message'], request.form['image'])
        data_manager.add_answer(form_data=new_answer)
        return redirect('/')
    question = data_manager.find_question(question_id)
    return render_template('new_answer.html', question=question, result=result, message=message)



def create_answer(question_id, message, image):
    return {
        'submission_time': data_manager.submission_time_generator(),
        'vote_number': 1,
        'question_id': question_id,
        'message': message,
        'image': image
    }

@app.route('/question_page/<answer_id>/update')
def edit_answer(answer_id):
    result = data_manager.find_answer(a_id=answer_id)
    return render_template('new_answer.html', result=result)


@app.route('/rewrite_answer', methods=['POST'])
def rewrite_answer():
    updated_answer = {
        'id': request.form.get('id'),
        'submission_time': request.form.get('submission_time'),
        'vote_number': request.form.get('vote_number'),
        'question_id': request.form.get('question_id'),
        'message': request.form.get('message'),
        'image': request.form.get('image'),
    }
    data_manager.update_answer(datas=updated_answer)
    return redirect('/')


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    result = []
    message = ""
    if request.method == 'POST':
        question_name = request.form.get('question_name')
        message = request.form.get('message')
        data_manager.add_question(message)
        return redirect('/')
    return render_template('add_question.html', message=message, result=result)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )

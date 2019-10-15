from flask import Flask, request, render_template, redirect, session,url_for
import data_manager

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/', methods=['GET', 'POST'])
def list_questions():
    if request.method == 'POST':
        session['username'] = request.form['username']

    if 'username' in session:
        login_name=session['username']
        is_logged_in=True
    else:
        login_name='None'
        is_logged_in = False

    data = data_manager.get_least_questions()
    return render_template('index.html', data=data, login_name=login_name,is_logged_in=is_logged_in)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('list_questions'))

@app.route('/search')
def search():
    search_result = data_manager.search(*request.args.values())
    return render_template('search.html', search_result=search_result)


@app.route('/list')
def show_all_questions():
    question_list = data_manager.get_all_questions()
    return render_template('list.html', question_list=question_list)


@app.route('/question/<question_id>')
def show_specific_question(question_id: int):
    question_data = data_manager.get_question_by_id(question_id)
    question_comment = data_manager.get_comments_for_question(question_id)
    question_answer = data_manager.get_answers_for_questions(question_id)
    return render_template('question_details.html', question_comment=question_comment,
                           question_answer=question_answer, question_data=question_data)


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_new_comment_to_question(question_id: int):
    question_data = data_manager.get_question_by_id(question_id)
    status = ''
    if request.method == 'POST':
        comment = request.form['comment']
        data_to_manager = [question_id, comment, 'question']
        data_manager.add_comment(data_to_manager)
        status = 'Comment added successfully'
    return render_template('add_comment.html', question_data=question_data, status=status,
                           question_id=question_id)


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def add_new_comment_to_answer(answer_id: int):
    #question_id = data_manager.get_question_id_by_answer_id(answer_id)
    answer_data = data_manager.get_answer_by_id(answer_id)
    answer_comment = data_manager.get_comments_for_answer(answer_id)
    status = ''
    if request.method == 'POST':
        comment = request.form['comment']
        data_to_manager = [answer_id, comment, 'answer']
        data_manager.add_comment(data_to_manager)
        status = 'Comment added successfully'
    return render_template('add_comment.html', answer_data=answer_data, status=status,
                           answer_comment=answer_comment)


@app.route('/question/<question_id>/add-answer', methods=['GET', 'POST'])
def add_answer(question_id: int):
    status = ''
    answer_data=data_manager.get_question_by_id(question_id)
    if request.method == 'POST':
        site_input = request.form['new-answer']
        data_manager.add_answer(site_input, question_id)
        status = 'Answer added successfully'
    return render_template('add_answer.html',question_id=question_id, answer_data=answer_data,
                           status=status)


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id: int):
    answer_data=data_manager.get_answer_by_id(answer_id)
    if request.method == 'POST':
        site_input = [request.form['new-answer']]
        site_input.append(answer_id)
        data_manager.edit_answer(site_input)
        return redirect('/list')
    return render_template('edit_answer.html',answer_data=answer_data)


@app.route('/add-question', methods=['GET','POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add_a_question.html')

    site_input = [request.form['title'], request.form['message']]
    data_manager.add_question(site_input)
    return redirect('/')


if __name__ == '__main__':
    app.run(
        debug=True
    )

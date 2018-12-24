import connection
from random import randint
from datetime import datetime
from psycopg2 import sql

#       QUESTIONS
# id: A unique identifier for the question
# submission_time: The UNIX timestamp when the question was posted
# view_number: How many times this question was displayed in the single question view
# vote_number: The sum of votes this question has received
# title: The title of the question
# message: The question text
# image: The path to the image for this question

#       ANSWERS
# id: A unique identifier for the answer
# submission_time: The UNIX timestamp when the answer was posted
# vote_number: The sum of votes this answer has received
# question_id: The id of the question this answer belongs to.
# message: The answer text
# image: the path to the image for this answer

# ----------------------------------------------------------
#                   get
# ----------------------------------------------------------


@connection.connection_handler
def get_all_questions(cursor):
    cursor.execute('SELECT * FROM question;')
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def get_latest_questions(cursor):
    cursor.execute('SELECT * FROM question ORDER BY submission_time DESC LIMIT 5;')
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute("SELECT * FROM question WHERE id='{0}';".format(question_id))
    question = cursor.fetchall()
    return question[0]


@connection.connection_handler
def get_question_id(cursor, answer_id):
    cursor.execute("SELECT question_id FROM answer WHERE id='{0}';".format(answer_id))
    question_id = cursor.fetchone()
    return question_id['question_id']


@connection.connection_handler
def get_answer_by_answer_id(cursor, answer_id):
    cursor.execute("SELECT * FROM answer WHERE id='{0}';".format(answer_id))
    answer = cursor.fetchall()
    return answer[0]


@connection.connection_handler
def get_answers_by_question_id(cursor, question_id):
    cursor.execute("SELECT * FROM answer WHERE question_id='{0}' ORDER BY vote_number DESC, submission_time DESC;".format(question_id))
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def get_answer_id(cursor, question_id):
    # answers = get_answers_by_question_id
    cursor.execute("SELECT id FROM answer WHERE question_id='{0}';".format(question_id))
    answer_ids = cursor.fetchall()
    return answer_ids


@connection.connection_handler
def get_comments_by_question_id(cursor, question_id):
    cursor.execute("SELECT * FROM comment WHERE question_id='{0}';".format(question_id))
    comment = cursor.fetchall()
    return comment



@connection.connection_handler
def get_comments_by_answer_id(cursor, answer_id):
    cursor.execute("SELECT * FROM comment WHERE answer_id='{0}';".format(answer_id))
    comment = cursor.fetchall()
    return comment


@connection.connection_handler
def get_comment_by_comment_id(cursor, comment_id):
    cursor.execute("SELECT * FROM comment WHERE id='{0}';".format(comment_id))
    comment = cursor.fetchall()
    return comment[0]


@connection.connection_handler
def get_all_answer_comments(cursor):
    cursor.execute(
        sql.SQL("SELECT * FROM comment").format(table=sql.Identifier('comment'))
    )
    comment = cursor.fetchall()
    return comment


@connection.connection_handler
def get_question_id_by_comment_id(cursor, comment_id):
    cursor.execute("SELECT question_id, answer_id FROM comment WHERE id='{0}';".format(comment_id))
    question_id = cursor.fetchone()
    if question_id['question_id'] == None:
        return get_question_id(question_id['answer_id'])
    return question_id['question_id']


# ----------------------------------------------------------
#                   add
# ----------------------------------------------------------


@connection.connection_handler
def new_answer(cursor, form, question_id):
    cursor.execute("INSERT INTO answer (submission_time, vote_number, question_id, message, image) VALUES ('{0}',0,'{1}','{2}','{3}');".format(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),question_id,form['message'],form['image']))
    return

@connection.connection_handler
def new_question(cursor, form):
    cursor.execute("INSERT INTO question (submission_time, view_number, vote_number, title, message, image) VALUES ('{0}',0, 0,'{1}','{2}','{3}');".format(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),form['title'],form['message'],form['image']))
    cursor.execute('''SELECT id FROM question ORDER BY submission_time DESC LIMIT 1''')
    question_id = cursor.fetchone()
    return question_id

@connection.connection_handler
def new_question_comment(cursor, form, question_id):
    cursor.execute("INSERT INTO comment (question_id, message, submission_time, edited_count) VALUES ('{0}', '{1}', '{2}', 0);".format(question_id, form['comment'], str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
    return question_id


@connection.connection_handler
def new_answer_comment(cursor, form, answer_id):
    cursor.execute("INSERT INTO comment (answer_id, message, submission_time, edited_count) VALUES ('{0}', '{1}', '{2}', 0);".format(answer_id, form['comment'], str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
    return answer_id

# ----------------------------------------------------------
#                   edit
# ----------------------------------------------------------

@connection.connection_handler
def edit_question(cursor, form, question_id):
    cursor.execute("UPDATE question SET submission_time='{0}',title='{1}',message='{2}',image='{3}' WHERE id={4};".format(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), form['title'], form['message'], form['image'], question_id))
    return


@connection.connection_handler
def edit_answer(cursor, form, answer_id):
    cursor.execute("UPDATE answer SET submission_time='{0}', message='{1}', image='{2}' WHERE id={3};".format(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), form['message'], form['image'], answer_id))
    return


@connection.connection_handler
def edit_comment(cursor, form, comment_id):
    cursor.execute("UPDATE comment SET message='{0}', submission_time='{1}', edited_count=edited_count+1 WHERE id={2};".format(form['comment'], str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), comment_id))

    return get_question_id_by_comment_id(comment_id)

# ----------------------------------------------------------
#                   delete
# ----------------------------------------------------------

@connection.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("DELETE FROM answer WHERE question_id='{0}'; DELETE FROM question WHERE id='{0}';".format(str(question_id)))
    return

@connection.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute("SELECT question_id FROM answer WHERE id='{0}';".format(str(answer_id)))
    question_id = cursor.fetchone()
    cursor.execute("DELETE FROM answer WHERE id='{0}';".format(str(answer_id)))
    return question_id['question_id']


@connection.connection_handler
def delete_comment(cursor, comment_id):
    cursor.execute("DELETE FROM comment WHERE id='{0}';".format(comment_id))
    return

# ----------------------------------------------------------
#                   vote
# ----------------------------------------------------------

# mode = answer | question
@connection.connection_handler
def vote(cursor, mode, direction, data_id):
    if direction == 'up':
        cursor.execute("UPDATE {0} SET vote_number=vote_number+1 WHERE id={1}".format(mode, data_id))
    if direction == 'down':
        cursor.execute("UPDATE {0} SET vote_number=vote_number-1 WHERE id={1}".format(mode, data_id))
    if mode == 'answer':
        cursor.execute("SELECT question_id FROM answer WHERE id='" + str(data_id) + "';")
        question_id = cursor.fetchone()['question_id']
        page_view_counter('down', question_id)
        return question_id
    page_view_counter('down', data_id)
    return

# ----------------------------------------------------------
#                   vote
# ----------------------------------------------------------

@connection.connection_handler
def page_view_counter(cursor, mode, question_id):
    if mode == 'up':
        cursor.execute("UPDATE question SET view_number=view_number+1 WHERE id={0}".format(question_id))
    if mode == 'down':
        cursor.execute("UPDATE question SET view_number=view_number-1 WHERE id={0}".format(question_id))
    return

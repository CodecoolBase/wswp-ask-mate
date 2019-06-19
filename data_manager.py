import connection
from datetime import datetime
import util
import os
from werkzeug.utils import secure_filename
from psycopg2 import sql


@connection.connection_handler
def get_data_from_db(cursor, table, order_by= None, order_direction=None):
    order_by = 'submission_time' if not order_by else order_by
    if order_direction == "desc":
        cursor.execute(
            sql.SQL("SELECT * FROM {table} ORDER BY {order_by} DESC").
                format(table=sql.Identifier(table),
                       order_by=sql.Identifier(order_by)))
    else:
        cursor.execute(
            sql.SQL("SELECT * FROM {table} ORDER BY {order_by}").
                format(table=sql.Identifier(table), order_by=sql.Identifier(order_by)))
    data = cursor.fetchall()
    return data


@connection.connection_handler
def add_question_to_db(cursor, data):
    cursor.execute("""
                    INSERT INTO question
                    (submission_time, view_number, vote_number, title, message, image)
                    VALUES(%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s);    
                    """,data)


@connection.connection_handler
def vote_question(cursor, vote, id):
    cursor.execute("""
        UPDATE question
        SET vote_number = vote_number + %(vote)s
        WHERE id=%(id)s;
        """, {'id': id, 'vote': vote})


@connection.connection_handler
def vote_answer(cursor, vote, id):
    cursor.execute("""
        UPDATE answer
        SET vote_number = vote_number + %(vote)s
        WHERE id=%(id)s;
        """, {'id': id, 'vote': vote})


@connection.connection_handler
def increment_view_number(cursor, item_id):
    cursor.execute('''
                    UPDATE question
                    SET view_number = (SELECT view_number
                                        FROM question
                                        WHERE id = %(question_id)s) + 1
                    WHERE id = %(question_id)s;
                    ''',
                   {'question_id': item_id})


def add_line_breaks_to_data(user_data):
    for data in user_data:
        for header, info in data.items():
            if type(info) == str:
                data[header] = info.replace('\n', '<br>')

    return user_data


@connection.connection_handler
def get_question_by_id(cursor,question_id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(question_id)s;
    """,{'question_id':question_id})

    question = cursor.fetchall()
    return question[0]


@connection.connection_handler
def get_answers_by_question_id(cursor, question_id):
    cursor.execute('''
                    SELECT *
                    FROM answer
                    WHERE question_id = %(question_id)s
                    ''',
                   {'question_id': question_id})
    searched_answers = cursor.fetchall()
    return searched_answers


def add_question(question, image_name):

    new_question = {}

    if image_name == '':
        image_path = ''
    else:
        image_path = f'{connection.UPLOAD_FOLDER}/{image_name}'

    for header,data in question.items():
        new_question[header] = data

    new_question_default = {'submission_time':datetime.now(),
                  'view_number': 0,
                  'vote_number': 0,
                  'image': image_path}
    for header, data in new_question_default.items():
        new_question[header] = data

    return new_question


@connection.connection_handler
def edit_question(cursor, data_to_edit, question_id):

    edited_data = {key:val for key, val in data_to_edit.items()}
    edited_data['question_id'] = question_id

    cursor.execute("""
                    UPDATE question
                    SET (title, message) = (%(title)s, %(message)s)
                    WHERE id = %(question_id)s;
    """,edited_data)


@connection.connection_handler
def add_answer(cursor, question_id, answer, image_name):
    if image_name == '':
        image_path = ''
    else:
        image_path = f'{connection.UPLOAD_FOLDER}/{image_name}'
    dt = datetime.now()
    cursor.execute('''
                    INSERT INTO answer
                    (submission_time, vote_number, question_id, message, image)
                    VALUES (%(time)s, %(vote_num)s, %(question_id)s, %(message)s, %(image)s);
                    ''',
                   {'time': dt,
                    'vote_num': 0,
                    'question_id': question_id,
                    'message': answer,
                    'image': image_path}
                   )


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in connection.ALLOWED_FILE_EXTENSIONS


def upload_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(connection.UPLOAD_FOLDER, filename))


def delete_answer_by_answer_id(answer_id):
    delete_from_table('comment', 'answer_id', answer_id)
    delete_from_table('answer', 'id', answer_id)


@connection.connection_handler
def get_question_id_by_answer_id(cursor, answer_id):
    cursor.execute("""
        SELECT question_id FROM answer
        WHERE id= %(answer_id)s;
    """, {'answer_id':answer_id})
    question_id = cursor.fetchall()
    if question_id:
        return question_id[0]['question_id']


def delete_question(question_id):
    delete_from_table('answer', 'question_id', question_id)
    delete_from_table('comment', 'question_id', question_id)
    tag_id = get_tag_ids(question_id)
    if tag_id:
        for id_ in tag_id:
            delete_from_table('tag', 'id', id_['tag_id'])
    delete_from_table('question_tag', 'question_id', question_id)
    delete_from_table('question', 'id', question_id)


@connection.connection_handler
def delete_from_table(cursor, table, parameter, value):
    cursor.execute(sql.SQL("DELETE FROM {0} WHERE {1} = %s")
                   .format(sql.Identifier(table),
                           sql.Identifier(parameter)), value)


def get_question_tags( question_id):
    tag_ids = get_tag_ids(question_id)
    tags = get_all_tags()
    if tag_ids:
        tags = [tag for tag in tags if tag['id'] in tag_ids]
    else:
        return None
    return tags


def get_rest_of_tags( question_id):
    tag_ids = get_tag_ids(question_id)
    tags = get_all_tags()
    if tag_ids:
        tags = [tag for tag in tags if tag['id'] not in tag_ids]

    return tags


@connection.connection_handler
def get_all_tags(cursor):
    cursor.execute("""
                        SELECT * FROM tag;
                    """)
    return cursor.fetchall()


@connection.connection_handler
def get_tag_ids(cursor, question_id):
    cursor.execute("""
        SELECT tag_id FROM question_tag WHERE question_id=%(question_id)s;
    """, {'question_id': question_id})
    tags = cursor.fetchall()
    if tags:
        tag_ids = tuple(tag['tag_id'] for tag in tags)

        return tag_ids


@connection.connection_handler
def add_tag(cursor, question_id, tag_id):
    cursor.execute("""
        INSERT INTO question_tag(question_id, tag_id)
        VALUES(%(question_id)s, %(tag_id)s);
    """, {'question_id':question_id,
          'tag_id':tag_id})


@connection.connection_handler
def remove_tag(cursor, question_id, tag_id):
    cursor.execute("""
        DELETE FROM question_tag
        WHERE tag_id=%(tag_id)s
        AND question_id= %(question_id)s;
    """, {'question_id':question_id,
          'tag_id':tag_id})
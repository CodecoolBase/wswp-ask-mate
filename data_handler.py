import connection
from psycopg2 import sql


@connection.connection_handler
def get_question_by_id(cursor, id):
    cursor.execute(
        """
        SELECT * FROM question WHERE id = %(id)s;
        """, {'id':int(id)})

    question = cursor.fetchall()
    return question[0]



@connection.connection_handler
def edit_questions(cursor, id, title, message, image):
    cursor.execute(
        """
        UPDATE question
        SET title = %(title)s, message = %(message)s, image = %(image)s
        WHERE id = %(id)s;
        """, {'title': title, 'id': int(id), 'message': message, 'image': image})


@connection.connection_handler
def get_last_5_questions_title(cursor, sort_by, direction):
    cursor.execute("""
                    SELECT title FROM question
                    ORDER BY %(sort_by)s %(direction)s
                    LIMIT 5;
                    """,
                   {'sort_by': sort_by, 'direction': direction})
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def get_all_questions_title(cursor, sort_by, direction):
    if direction == "ASC":
        cursor.execute(sql.SQL("""
                            SELECT title FROM question
                            ORDER BY {sort_by} ASC;
                            """
                            ).format(sort_by=sql.Identifier(sort_by)),
                       {'sort_by': sort_by})
    else:
        cursor.execute(sql.SQL("""
                                    SELECT title FROM question
                                    ORDER BY {sort_by} DESC;
                                    """
                               ).format(sort_by=sql.Identifier(sort_by)),
                       {'sort_by': sort_by})

    questions = cursor.fetchall()
    return questions

@connection.connection_handler
def get_question_n_answers_by_question_id(cursor, id):
    cursor.execute("""
                    SELECT * FROM question
                    JOIN answer ON question.id = answer.question_id
                    WHERE id == id;
                    """,
                   {'id': id})
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def delete_question(cursor, id):
    cursor.execute("""
                    DELETE FROM question
                    WHERE id = %(id)s
                    """,
                   {'id': id})


@connection.connection_handler
def insert_data_to_question(cursor, submission_time, view_number, vote_number, title, message, image):
    cursor.execute("""
                    INSERT INTO question
                    (submission_time, view_number, vote_number, title, message, image)
                    VALUES (%s, %s, %s, %s, %s, %s);""",
                   (submission_time, view_number, vote_number, title, message, image))

@connection.connection_handler
def insert_data_to_answer(cursor, submission_time, view_number, question_id, message, image):
    cursor.execute("""
                    INSERT INTO answer
                    (submission_time, view_number, question_id message, image)
                    VALUES (%s, %s, %s, %s, %s);""",
                   (submission_time, view_number, question_id, message, image))


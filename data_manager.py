import database_connection
import util
from datetime import datetime

@database_connection.connection_handler
def list_all_question(cursor):
    cursor.execute("""
                    SELECT * FROM Question
                    ORDER BY submission_time DESC;
                    """)
    all_question = cursor.fetchall()
    return all_question

@database_connection.connection_handler
def list_answers(cursor):
    cursor.execute("""
                    SELECT * FROM answer; 
    """)
    all_answer = cursor.fetchall()
    return all_answer


def count_answers(quest_id):
    any_answer = list_answers()
    return any(answer['question_id'] == int(quest_id) for answer in any_answer)


@database_connection.connection_handler
def ask_new_question(cursor, title, message):
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, vote_number, title, message)
                    VALUES (%(dt)s, 1, 0, %(add_title)s, %(add_message)s)
                    """, dict(dt=dt, add_title=title, add_message=message))



@database_connection.connection_handler
def update_question(cursor, title, message, quest_id):
    cursor.execute("""
                    UPDATE question
                    SET title = %(title)s, message = %(message)s
                    WHERE id = %(quest_id)s
                    """, dict(title=title, message=message, quest_id=quest_id))


@database_connection.connection_handler
def delete_question(cursor, quest_id):
    cursor.execute("""
                    DELETE FROM question
                    WHERE id = %(quest_id)s
                    """, dict(quest_id=quest_id))


@database_connection.connection_handler
def get_latest_id(cursor):
    cursor.execute("""
                    SELECT id FROM question
                    ORDER BY id DESC
                    LIMIT 1 
                    """)
    return cursor.fetchone()

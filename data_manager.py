import connection
import util


QUESTION_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]

question_file = "./sample_data/question.csv"
answer_file = "./sample_data/answer.csv"

def get_single_line_by_id(story_id, filename):
    """Reads single answer or question from file by the given ID. Returns dictionary."""
    all_stories = connection.read_file(filename)

    for story in all_stories:

        if story["id"] == story_id:
            story["submission_time"] = util.convert_unix_time_to_readable(story["submission_time"])
            return story



"""decorator function, sorts data by given key and order"""
def sort_dict(func):
    def wrapper(*args, reverse=True, key="submission_time"):
        data = func(*args)
        array = sorted(data, key=lambda x: x[key], reverse=reverse)
        return array
    return wrapper


@sort_dict
def get_all_questions(filename):
    """ returns a dictionary, has sorting decorator function.
    ARGS:
        filename (string),
        reverse=False (boolean): decorator keyname parameter with default value,
        key="submission_time" (string): decorator keyname paramtere with default value,
    """
    all_questions = connection.read_file(filename)
    modded_questions = []

    for question in all_questions:
        question["submission_time"] = util.convert_unix_time_to_readable(question["submission_time"])
        modded_questions.append(question)

    return modded_questions


def get_csv_file(filename):
    return connection.read_file(filename)


def get_answers_to_question(question_id, answers_file):
    """Reads 'answer_file' to find any answers that have the 'question_id'."""
    all_answers = connection.read_file(answers_file)
    answers_to_question = []

    for answer in all_answers:
        if answer["question_id"] == question_id:
            answer["submission_time"] = util.convert_unix_time_to_readable(answer["submission_time"])
            answers_to_question.append(answer)

    return answers_to_question


def modify_vote_story(story_id, filename, vote_method):
    story = get_single_line_by_id(story_id,filename)
    vote_number = int(story["vote_number"])
    if vote_method == "up":
        vote_number += 1
    elif vote_number == "down":
        vote_number -= 1

    story["vote_number"] = int(vote_number)
    story_to_update = story

    return story_to_update


def fill_out_missing_data(new_data):
    """Fills out the missing data in the new question/answer(id, date, view number, vote number)"""
    new_data['submission_time'] = util.get_unix_time()
    new_data['view_number'] = 0
    new_data['vote_number'] = 0
    return new_data

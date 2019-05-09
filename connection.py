import csv


def read_data(filename):
    with open(filename, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        datas = reversed(list(reader))
    return datas

def append_data(filename, story, KEYS):
    with open(filename, "a") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=KEYS)
        writer.writerow(story)

def write_data(filename, fieldnames, datas):
    with open(filename, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for data in datas:
            writer.writerow(data)

def delete_answer(answer_id, KEYS, filename="sample_data/answer.csv"):
    answers = read_data(filename)
    with open(filename, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=KEYS)
        writer.writeheader()
        for answer in answers:
            if answer["id"] != answer_id:
                writer.writerow(answer)
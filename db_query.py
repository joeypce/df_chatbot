import sqlite3
from sqlite3 import Error
import os

dirname = os.path.dirname(__file__)
db_filename = os.path.join(dirname, 'db.sqlite3')
print("database sqllite3 " + db_filename)

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

database = db_filename

# not in use, test basic function of db
def select_question_answer():
    conn = create_connection(database)
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT question, answer FROM ambiguity_table")

        rows = cur.fetchall()

        for row in rows:
            print(row)


def select_suggestions_by_keyword(kw):
    conn = create_connection(database)
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT question FROM ambiguity_table WHERE question LIKE ? LIMIT 5", ('%'+kw+'%',))
        rows = cur.fetchall()
        question_suggestions = []
        for row in rows:
            # row = row.replace("(", "")
            question_suggestions.append(row)
            # print(row)
        return question_suggestions

def select_response_for_beta(questiontype, kw):
    #remove empty string
    kw1 = filter(None, kw)
    kw1 = [x.strip(' ') for x in kw1]

    kw_string = ' '.join(kw1)
    print(kw_string)
    conn = create_connection(database)
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT answer FROM beta WHERE question_type=? AND question LIKE ? LIMIT 1", (questiontype, kw_string+'%',))
        rows = cur.fetchall()
        print(rows)
        answers = []
        for row in rows:
            answers.append(row)
        return answers

def select_response_for_charlie(intent, kw):
    #remove empty string
    kw1 = filter(None, kw)
    kw1 = [x.strip(' ') for x in kw1]

    kw_string = ' '.join(kw1)
    print(kw_string)
    conn = create_connection(database)
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT answer FROM charlie WHERE theme=? AND foreign_key LIKE ? LIMIT 1", (intent, kw_string+'%',))
        rows = cur.fetchall()
        print(rows)
        answers = []
        for row in rows:
            answers.append(row)
        return answers


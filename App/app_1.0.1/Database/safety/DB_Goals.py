import sqlite3
from sqlite3 import Error

import Constant
from Objects.Goal import Goal


# make a connection
def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(Constant.DB_FILE)
    except Error as e:
        print(e)

    return conn


# create all tables if not exists
def create_table():
    sql_create_goals_table = "CREATE TABLE IF NOT EXISTS goals (id INTEGER PRIMARY KEY AUTOINCREMENT, id_project INTEGER NOT NULL, id_goal INTEGER NOT NULL, " \
                             "description TEXT NOT NULL, begin_date TEXT NOT NULL, edited_date TEXT, " \
                             "FOREIGN KEY(id_project) REFERENCES projects(id));"

    return sql_create_goals_table




# insert one register to Table Goals
def insert_to_goals(goal):
    # create a database connection
    conn = create_connection()
    with conn:
        sql = "INSERT INTO goals(id_project, id_goal, description, begin_date) VALUES(?, ?, ?, ?)"
        cur = conn.cursor()
        task = (goal.id_project, goal.id_goal, goal.description, goal.begin_date)
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid


# update one register to Table Goals
def update_goal(goal):
    # create a database connection
    conn = create_connection()
    with conn:
        sql = "UPDATE goals SET description = ?, edited_date = ? WHERE id = ?"
        cur = conn.cursor()
        task = (goal.description, goal.edited_date, goal.id)
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid


# update one register to Table Goals
def delete_goal(goal):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM goals WHERE id = ?", (goal.id,))
        conn.commit()
        return cur.lastrowid

# select all projects ordering by id_goal
def select_all_goals_by_project(id_project):
    """
    Query tasks by all rows
    :return: List of Goals
    """
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM goals WHERE id_project = ? ORDER BY id_goal", (id_project,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Goal(row[0], row[1], row[2], row[3], row[4], row[5]))

    return result_list

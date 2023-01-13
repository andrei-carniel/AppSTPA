import sqlite3
from sqlite3 import Error

import Constant
from Objects.Assumptions import Assumptions
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
    sql_table = "CREATE TABLE IF NOT EXISTS assumptions (id INTEGER PRIMARY KEY AUTOINCREMENT, id_project INTEGER NOT NULL, " \
                             "id_assumption INTEGER NOT NULL, description TEXT NOT NULL, begin_date TEXT NOT NULL, edited_date TEXT, " \
                             "FOREIGN KEY(id_project) REFERENCES projects(id));"

    return sql_table


# insert one register to Table Goals
def insert_to_assumptions(assump):
    # create a database connection
    conn = create_connection()
    with conn:
        sql = "INSERT INTO assumptions (id_project, id_assumption, description, begin_date) VALUES (?, ?, ?, ?)"
        cur = conn.cursor()
        task = (assump.id_project, assump.id_assumption,  assump.description,  assump.begin_date)
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid


# update one register to Table Goals
def update_assumption(assump):
    # create a database connection
    conn = create_connection()
    with conn:
        sql = "UPDATE assumptions SET description = ?, edited_date = ? WHERE id = ?"
        cur = conn.cursor()
        task = (assump.description, assump.edited_date, assump.id)
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid


# update one register to Table Goals
def delete_assumption(assump):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM assumptions WHERE id = ?", (assump.id,))
        conn.commit()
        return cur.lastrowid


# select all projects ordering by id_goal
def select_all_assumptions_by_project(id_project):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM assumptions WHERE id_project = ?", (id_project,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Assumptions(row[0], row[1], row[2], row[3], row[4], row[5]))

    return result_list

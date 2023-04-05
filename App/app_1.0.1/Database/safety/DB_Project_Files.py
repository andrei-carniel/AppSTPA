import sqlite3
from sqlite3 import Error

import Constant


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
    sql_create_projects_table = "CREATE TABLE IF NOT EXISTS project_files(id INTEGER PRIMARY KEY AUTOINCREMENT, id_project INTEGER NOT NULL, " \
                                "identification TEXT NOT NULL, file_path TEXT NOT NULL, creation_date TEXT NOT NULL, order_file INTEGER NOT NULL DEFAULT 1, " \
                                "FOREIGN KEY(id_project) REFERENCES projects(id));"

    return sql_create_projects_table

# insert one register to Table Projects
def insert_control_srtucture_file(id_project, file_path, current_date, order_file):
    # create a database connection
    conn = create_connection()
    with conn:
        sql = "INSERT INTO project_files (id_project, identification, file_path, creation_date, order_file) VALUES(?, ?, ?, ?, ?)"

        cur = conn.cursor()
        cur.execute("DELETE FROM project_files WHERE id_project = ? AND identification = 'STPA_2' AND order_file = ?", (id_project, order_file,))
        cur.execute(sql, (id_project, "STPA_2", file_path, current_date, order_file))
        conn.commit()
        return cur.lastrowid

def delete_file(id_project, order_file):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM project_files WHERE id_project = ? AND identification = 'STPA_2' AND order_file = ?", (id_project, order_file,))

        conn.commit()
        return cur.lastrowid

# select all projects ordering by name
def select_images_by_project(id_project, order_file):
    """
    Query tasks by all rows
    :return: List of Projects
    """
    result = ""

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT file_path FROM project_files WHERE id_project = ? AND identification = 'STPA_2' AND order_file = ?", (id_project, order_file,))

        row = cur.fetchone()
        if row != None:
            result = row[0]

    return result

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

# return the sql query for components
def create_table():
    sql_query = "CREATE TABLE IF NOT EXISTS saf_priority (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL);"

    return sql_query

# insert the default data on stride
def insert_stride(conn):
    sql = "INSERT OR REPLACE INTO saf_priority(id, name) VALUES(?, ?)"

    rsql1 = insert_to_db(conn, sql, (Constant.DB_ID_HIGH, Constant.DB_NAME_HIGH))
    rsql2 = insert_to_db(conn, sql, (Constant.DB_ID_MEDIUM, Constant.DB_NAME_MEDIUM))
    rsql3 = insert_to_db(conn, sql, (Constant.DB_ID_LOW, Constant.DB_NAME_LOW))

# insert many registers to Table Things
def insert_to_db(conn, sql, task):
    # create a database connection
    try:
        with conn:
            cur = conn.cursor()
            cur.execute(sql, task)
            conn.commit()
            return cur.lastrowid
    except Error as e:
        print(e)

# select action name
def select_all():
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM saf_priority")

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Stride_Priority(row[0], row[1]))

    return result_list

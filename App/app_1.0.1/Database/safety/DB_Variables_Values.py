import sqlite3
from sqlite3 import Error

import Constant
from Objects.Action import Action,Action_Component
from Objects.Component import Component
from Objects.Loss import Loss


# make a connection
from Objects.Variables import Variables
from Objects.Variable_Values import Variable_Values


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
    sql_query = "CREATE TABLE IF NOT EXISTS variables_values (id INTEGER PRIMARY KEY AUTOINCREMENT, id_variable INTEGER NOT NULL, " \
                "value TEXT NOT NULL, begin_date TEXT NOT NULL, edited_date TEXT, " \
                "FOREIGN KEY(id_variable) REFERENCES variables(id) " \
                ");"

    return sql_query

def insert(value):
    conn = create_connection()
    with conn:
        sql = "INSERT INTO variables_values (id_variable, value, begin_date) VALUES(?, ?, ?)"
        cur = conn.cursor()
        task = (value.id_variable, value.value, value.begin_date)
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid

def update(val):
    # create a database connection
    conn = create_connection()
    with conn:
        sql = "UPDATE variables_values SET value = ?, edited_date = ? WHERE id = ?"
        cur = conn.cursor()
        task = (val.value, val.edited_date, val.id)
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid

def delete(val):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM variables_values WHERE id = ?", (val.id,))
        conn.commit()
        return cur.lastrowid

def delete_by_variable(var_id):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM variables_values WHERE id_variable = ?", (var_id,))
        conn.commit()
        return cur.lastrowid

# select all losses ordering by id_loss
# def select_all_components_by_project_analysis(id_project, id_analysis):
#     """
#     Query tasks by all rows
#     :return: List of Losses
#     """
#     result_list = []
#
#     # create a database connection
#     conn = create_connection()
#     with conn:
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM losses WHERE id_project = ? ORDER BY id_loss", (id_project,))
#
#         rows = cur.fetchall()
#
#         for row in rows:
#             result_list.append(Action_Component(row[0], row[1], row[2], row[3], row[4]))
#
#     return result_list



# select all losses ordering by id_loss
def select_values_by_variable(id_variable):
    """
    Query tasks by all rows
    :return: List of Losses
    """
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM variables_values WHERE id_variable = ?", (id_variable,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Variable_Values(row[0], row[1], row[2], row[3], row[4]))


    return result_list
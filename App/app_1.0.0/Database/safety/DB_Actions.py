import sqlite3
from sqlite3 import Error

import Constant
from Objects.Action import Action
from Objects.Component import Component
from Objects.Loss import Loss


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
    sql_query = "CREATE TABLE IF NOT EXISTS actions (id INTEGER PRIMARY KEY AUTOINCREMENT, source INTEGER NOT NULL, destiny INTEGER NOT NULL, " \
                "name TEXT NOT NULL, name_ontology TEXT NOT NULL, name_link TEXT NOT NULL, " \
                "FOREIGN KEY(source) REFERENCES things(id) " \
                "FOREIGN KEY(destiny) REFERENCES things(id));"

    return sql_query

# insert one register to Table Loss
# def insert_to_components(component):
    # create a database connection
    # conn = create_connection()
    # with conn:
    #     sql = "INSERT INTO losses(id_project, id_loss, description, begin_date) VALUES(?, ?, ?, ?)"
    #     cur = conn.cursor()
    #     task = (loss.id_project, loss.id_loss, loss.description, loss.begin_date)
    #     cur.execute(sql, task)
    #     conn.commit()
    #     return cur.lastrowid


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


# select action by name
def select_action_by_name(name):
    """
    Query tasks by all rows
    :return: List of Losses
    """
    result = None

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM actions WHERE name_ontology = ?", (name,))

        row = cur.fetchone()

        if row != None:
            result = Action(row[0], row[1], row[2], row[3], row[4], row[5])

    return result


# select action name
def select_name_by_name_ontology(name):
    result = ""

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT a.name FROM actions AS a WHERE a.name_ontology = ?", (name,))

        row = cur.fetchone()

        if row != None:
            result = row[0]

    return result


# select all actions component by action name
def select_action_by_name_with_component(name_action, id_project):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT a.id, a.source, a.destiny, a.name, a.name_ontology, a.name_link, c.name FROM actions AS a "
                    "JOIN components AS c ON a.source = c.id_thing "
                    "WHERE a.name_ontology = ? AND c.id_project = ? ", (name_action, id_project,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Action(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    return result_list
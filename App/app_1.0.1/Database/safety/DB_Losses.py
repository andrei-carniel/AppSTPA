import sqlite3
from sqlite3 import Error

import Constant
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


# create all tables if not exists
def create_table():
    sql_create_losses_table = "CREATE TABLE IF NOT EXISTS losses(id INTEGER PRIMARY KEY AUTOINCREMENT, id_project INTEGER NOT NULL, id_loss INTEGER NOT NULL, " \
                              "description TEXT NOT NULL, begin_date TEXT NOT NULL, edited_date TEXT, " \
                              "FOREIGN KEY(id_project) REFERENCES projects(id) );"

    return sql_create_losses_table

# insert one register to Table Loss
def insert_to_losses(loss):
    # create a database connection
    conn = create_connection()
    with conn:
        sql = "INSERT INTO losses(id_project, id_loss, description, begin_date) VALUES(?, ?, ?, ?)"
        cur = conn.cursor()
        task = (loss.id_project, loss.id_loss, loss.description, loss.begin_date)
        cur.execute(sql, task)
        conn.commit()
        id_saved = cur.lastrowid

        update_loss_id(loss.id_project)

        return id_saved

# insert one register to Table Loss
def update_loss_id(id_project):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM losses WHERE id_project = ?", (id_project,))
        rows = cur.fetchall()
        count = 1
        for row in rows:
            cur.execute("UPDATE losses SET id_loss = ? WHERE id = ?", (count, row[0],))
            count += 1
        conn.commit()

# update one register to Table Goals
def update_loss(loss):
    # create a database connection
    conn = create_connection()
    with conn:
        sql = "UPDATE losses SET description = ?, edited_date = ? WHERE id = ?"
        cur = conn.cursor()
        task = (loss.description, loss.edited_date, loss.id)
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid


# update one register to Table Goals
def delete_loss(loss):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM losses WHERE id = ?", (loss.id,))
        conn.commit()
        id_saved = cur.lastrowid

        update_loss_id(loss.id_project)

        return id_saved


# select all losses ordering by id_loss
def select_all_losses_by_project(id_project):
    """
    Query tasks by all rows
    :return: List of Losses
    """
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM losses WHERE id_project = ? ORDER BY id_loss", (id_project,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Loss(row[0], row[1], row[2], row[3], row[4], row[5]))

    return result_list

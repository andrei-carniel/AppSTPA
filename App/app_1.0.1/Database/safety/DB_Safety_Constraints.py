import sqlite3
from sqlite3 import Error

import Constant


# make a connection
from Objects.Safety_Constraint import Safety_Constraint, Safety_Constraint_Hazard


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
def create_all_tables_safety_constraints():
    sql_create_safety_constraints_table = "CREATE TABLE IF NOT EXISTS safety_constraints (id INTEGER PRIMARY KEY AUTOINCREMENT, id_project INTEGER NOT NULL, " \
                                          "id_safety_constraint INTEGER NOT NULL, description TEXT NOT NULL, begin_date TEXT NOT NULL, " \
                                          "edited_date TEXT, " \
                                          "FOREIGN KEY(id_project) REFERENCES projects(id) );"

    return sql_create_safety_constraints_table


# create all tables if not exists
def create_all_tables_safety_constraints_hazards():
    sql_create_safety_constraints_table = "CREATE TABLE IF NOT EXISTS safety_constraints_hazards (id INTEGER PRIMARY KEY AUTOINCREMENT, id_project INTEGER NOT NULL, " \
                                          "id_constraint INTEGER NOT NULL, id_hazard INTEGER NOT NULL, " \
                                          "FOREIGN KEY(id_project) REFERENCES projects(id) " \
                                          "FOREIGN KEY(id_hazard) REFERENCES hazards(id) " \
                                          "FOREIGN KEY(id_constraint) REFERENCES safety_constraints(id) );"

    return sql_create_safety_constraints_table


# insert one register to Table Safety Constraints
def insert_to_safety_constraints(constraint):

    # create a database connection
    conn = create_connection()
    with conn:
        sql = "INSERT INTO safety_constraints(id_project, id_safety_constraint, description, begin_date) VALUES(?, ?, ?, ?)"
        cur = conn.cursor()
        task = (constraint.id_project, constraint.id_safety_constraint, constraint.description, constraint.begin_date)
        result = cur.execute(sql, task)
        id_ssc = result.lastrowid
        conn.commit()

        for cons_haz in constraint.list_of_hazards:
            cons_haz.id_constraint = id_ssc
            insert_to_constraint_hazard(cons_haz)

        return cur.lastrowid


# insert one register to Table Hazards
def insert_to_constraint_hazard(cons_haz):
    # create a database connection
    conn = create_connection()
    with conn:
        sql = "INSERT INTO safety_constraints_hazards(id_project, id_constraint, id_hazard) VALUES(?, ?, ?)"

        cur = conn.cursor()
        task = (cons_haz.id_project, cons_haz.id_constraint, cons_haz.id_hazard)
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid


# update one register to Table Goals
def update_safety_constraints(ssc):
    # create a database connection
    conn = create_connection()
    with conn:
        sql = "UPDATE safety_constraints SET description = ?, edited_date = ? WHERE id = ?"
        cur = conn.cursor()
        task = (ssc.description, ssc.edited_date, ssc.id)
        cur.execute(sql, task)

        cur.execute("DELETE FROM safety_constraints_hazards WHERE id_constraint = ?", (ssc.id,))
        sql = "INSERT INTO safety_constraints_hazards(id_project, id_constraint, id_hazard) VALUES(?, ?, ?)"

        for haz in ssc.list_of_hazards:
            cur = conn.cursor()
            task = (haz.id_project, haz.id_constraint, haz.id_hazard)
            cur.execute(sql, task)

        conn.commit()
        return cur.lastrowid


def delete_safety_constraints(ssc):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM safety_constraints WHERE id = ?", (ssc.id,))
        conn.commit()
        delete_constrain_hazard(ssc)
        return cur.lastrowid


def delete_constrain_hazard(ssc):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM safety_constraints_hazards WHERE id_constraint = ?", (ssc.id,))
        conn.commit()
        return cur.lastrowid

# select all hazards by id_project
def select_all_safety_constraints_by_project(id_project):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM safety_constraints WHERE id_project = ? ORDER BY id_safety_constraint", (id_project,))

        rows = cur.fetchall()

        for row in rows:
            ssc = Safety_Constraint(row[0], row[1], row[2], row[3], row[4], row[5])

            cur.execute("SELECT sch.id, sch.id_project, sch.id_constraint, sch.id_hazard, h.id_hazard FROM safety_constraints_hazards AS sch "
                        "JOIN hazards AS h ON h.id = sch.id_hazard "
                        "WHERE sch.id_project = ? AND sch.id_constraint = ? "
                        "ORDER BY h.id_hazard", (id_project, ssc.id))

            rows_haz = cur.fetchall()
            result_haz_list = []
            for row_haz in rows_haz:
                result_haz_list.append(Safety_Constraint_Hazard(row_haz[0], row_haz[1], row_haz[2], row_haz[3], row_haz[4]))

            ssc.list_of_hazards = result_haz_list
            result_list.append(ssc)



    return result_list


# select all hazards by id_project and id_loss
def select_all_safety_constraints_by_project_and_hazard(id_project, id_hazard):
    """
    Query tasks by all rows
    :return: List of Goals
    """
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM safety_constraints WHERE id_project = ? and id_hazard = ? ORDER BY id_safety_constraint", (id_project, id_hazard,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Safety_Constraint(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    return result_list

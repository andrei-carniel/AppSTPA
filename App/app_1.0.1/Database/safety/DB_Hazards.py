import sqlite3
from sqlite3 import Error

import Constant
from Objects.Hazard import Hazard, Hazard_Loss
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
def create_table_hazards():
    sql_create_hazards_table = "CREATE TABLE IF NOT EXISTS hazards(id INTEGER PRIMARY KEY AUTOINCREMENT, id_project INTEGER NOT NULL, " \
                               "id_hazard INTEGER NOT NULL, description TEXT NOT NULL, begin_date TEXT NOT NULL, edited_date TEXT, " \
                               "FOREIGN KEY(id_project) REFERENCES projects(id) );"

    return sql_create_hazards_table

# create all tables if not exists
def create_table_hazards_losses():
    sql_create_hazards_table = "CREATE TABLE IF NOT EXISTS hazards_losses (id INTEGER PRIMARY KEY AUTOINCREMENT, id_project INTEGER NOT NULL, " \
                               "id_hazard INTEGER NOT NULL, id_loss INTEGER NOT NULL, " \
                               "FOREIGN KEY(id_project) REFERENCES projects(id) " \
                               "FOREIGN KEY(id_hazard) REFERENCES hazards(id) " \
                               "FOREIGN KEY(id_loss) REFERENCES losses(id) );"

    return sql_create_hazards_table


# insert one register to Table Hazards
def insert_to_hazards(hazard):

    # create a database connection
    conn = create_connection()
    with conn:
        sql = "INSERT INTO hazards(id_project, id_hazard, description, begin_date) VALUES(?, ?, ?, ?)"

        cur = conn.cursor()
        task = (hazard.id_project, hazard.id_hazard, hazard.description, hazard.begin_date)
        result = cur.execute(sql, task)
        id_hazard = result.lastrowid
        conn.commit()

        for loss in hazard.list_of_loss:
            loss.id_hazard = id_hazard
            insert_to_hazard_losses(loss)

        id_saved = cur.lastrowid
        update_hazard_id(hazard.id_project)
        return id_saved


# insert one register to Table Loss
def update_hazard_id(id_project):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM hazards WHERE id_project = ?", (id_project,))
        rows = cur.fetchall()
        count = 1
        for row in rows:
            cur.execute("UPDATE hazards SET id_hazard = ? WHERE id = ?", (count, row[0],))
            count += 1
        conn.commit()

# insert one register to Table Hazards
def insert_to_hazard_losses(hazard_loss):
    # create a database connection
    conn = create_connection()
    with conn:
        sql = "INSERT INTO hazards_losses(id_project, id_hazard, id_loss) VALUES(?, ?, ?)"

        cur = conn.cursor()
        task = (hazard_loss.id_project, hazard_loss.id_hazard, hazard_loss.id_loss)
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid

# update one register to Table Goals
def update_hazard(hazard):
    # create a database connection
    conn = create_connection()
    with conn:
        sql = "UPDATE hazards SET description = ?, edited_date = ? WHERE id = ?"
        cur = conn.cursor()
        task = (hazard.description, hazard.edited_date, hazard.id)
        cur.execute(sql, task)

        cur.execute("DELETE FROM hazards_losses WHERE id_hazard = ?", (hazard.id,))
        sql = "INSERT INTO hazards_losses(id_project, id_hazard, id_loss) VALUES(?, ?, ?)"

        for loss in hazard.list_of_loss:
            cur = conn.cursor()
            task = (loss.id_project, loss.id_hazard, loss.id_loss)
            cur.execute(sql, task)

        conn.commit()
        return cur.lastrowid

# update one register to Table Goals
def delete_hazard(hazard):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM hazards WHERE id = ?", (hazard.id,))
        cur.execute("DELETE FROM hazards_losses WHERE id_hazard = ?", (hazard.id,))
        conn.commit()
        id_saved = cur.lastrowid
        update_hazard_id(hazard.id_project)
        return id_saved

# select all hazards by id_project
def select_all_hazards_by_project(id_project):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM hazards WHERE id_project = ? ORDER BY id_hazard", (id_project,))

        rows = cur.fetchall()

        for row in rows:
            haz = Hazard(row[0], row[1], row[2], row[3], row[4], row[5])

            cur.execute("SELECT hl.id, hl.id_project, hl.id_hazard, hl.id_loss, l.id_loss FROM hazards_losses AS hl "
                        "JOIN losses AS l ON l.id = hl.id_loss "
                        "WHERE hl.id_project = ? AND hl.id_hazard = ? ORDER BY l.id_loss", (id_project, haz.id))

            rows_losses = cur.fetchall()
            result_loss_list = []
            for row_loss in rows_losses:
                result_loss_list.append(Hazard_Loss(row_loss[0], row_loss[1], row_loss[2], row_loss[3], row_loss[4]))

            haz.list_of_loss = result_loss_list
            result_list.append(haz)


    return result_list


# select all hazards by id_project and id_loss
def select_all_hazards_by_project_and_loss(id_project, id_loss):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM hazards WHERE id_project = ? and id_loss = ? ORDER BY id_hazard", (id_project, id_loss,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Hazard(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    return result_list


# select all hazards by id_project with id loss
def select_all_hazards_by_project_with_loss(id_project):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT h.id, h.id_project, h.id_loss, h.id_hazard, h.description, h.begin_date, h.edited_date, l.id_loss FROM hazards AS h "
                    "JOIN losses AS l ON h.id_loss = l.id "
                    "WHERE h.id_project = ?", (id_project,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Hazard(row[0], row[1], row[2], row[3], row[4], row[5], row[6],row[7]))

    return result_list




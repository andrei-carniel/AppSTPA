import sqlite3
from sqlite3 import Error

import Constant
from Database.safety import DB_UCA
from Objects.Action import Action_Component
from Objects.Component import Component
from Objects.Component_Actions_Aux import Component_Actions


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
    # sql_query = "CREATE TABLE IF NOT EXISTS actions_component (id INTEGER PRIMARY KEY AUTOINCREMENT, id_component_src INTEGER NOT NULL, id_component_dst INTEGER NOT NULL, name TEXT NOT NULL, begin_date TEXT NOT NULL, edited_date TEXT, id_component_link INTEGER NOT NULL, id_project INTEGER NOT NULL, FOREIGN KEY(id_component_src) REFERENCES components(id) FOREIGN KEY(id_component_dst) REFERENCES components(id) FOREIGN KEY(id_component_link) REFERENCES components_links(id) FOREIGN KEY(id_project) REFERENCES projects(id) );"

    sql_query = "CREATE TABLE IF NOT EXISTS actions_component (id INTEGER PRIMARY KEY AUTOINCREMENT, id_component_src INTEGER NOT NULL, name TEXT NOT NULL, " \
                "begin_date TEXT NOT NULL, edited_date TEXT, id_project INTEGER NOT NULL, " \
                "FOREIGN KEY(id_project) REFERENCES projects(id), " \
                "FOREIGN KEY(id_component_src) REFERENCES components(id) )"

    return sql_query

# insert one register to Table Loss
def insert_to_table(act):
    conn = create_connection()
    with conn:
        sql = "INSERT INTO actions_component (id_component_src, name, begin_date, id_project) VALUES(?, ?, ?, ?)"
        cur = conn.cursor()
        task = (act.id_component_src, act.name, act.begin_date, act.id_project)
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid

# update one register to Table Goals
def update(act):
    # create a database connection
    conn = create_connection()
    with conn:
        sql = "UPDATE actions_component SET name = ?, edited_date = ? WHERE id = ?"
        cur = conn.cursor()
        task = (act.name, act.edited_date, act.id)
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid


# update one register to Table
def delete(act):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM actions_component WHERE id = ?", (act.id,))
        conn.commit()
        DB_UCA.delete_by_control_action(act.id)
        return cur.lastrowid

# update one register to Table Goals
def delete_by_controller(id_source):
    list_uca = select_id_actions_by_controller(id_source)
    # create a database connection
    conn = create_connection()

    with conn:

        cur = conn.cursor()
        cur.execute("DELETE FROM actions_component WHERE id_component_src = ?", (id_source,))

        for id_control_action in list_uca:
            list_id_uca = DB_UCA.select_id_uca_by_control_action(id_control_action)

            for id_uca in list_id_uca:
                cur.execute("DELETE FROM saf_loss_scenario_req where id_uca = ?", (id_uca,))
                cur.execute("DELETE FROM saf_uca_hazard WHERE id_uca = ?", (id_uca,))
                cur.execute("DELETE FROM saf_uca_context WHERE id_uca = ?", (id_uca,))
                cur.execute("DELETE FROM saf_uca WHERE id = ?", (id_uca,))


        conn.commit()
        return cur.lastrowid

# select all actions by component and action
def select_actions_by_component_and_action(id_component, id_action):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM actions_component WHERE id_component_src = ? AND id_action = ?", (id_component, id_action))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Action_Component(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    return result_list

#  select all actions by component source
def select_actions_by_component_and_project(id_component_src, id_project):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM actions_component WHERE id_component_src = ? AND id_project = ?", (id_component_src, id_project,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Action_Component(row[0], row[1], row[2], row[3], row[4], row[5]))

    return result_list

#  select all actions by component source and component destiny
def select_actions_by_component_and_project_and_destiny(id_component_src, id_project, id_component_dst):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT ac.id, ac.id_component_src, ac.name, ac.begin_date, ac.edited_date, ac.id_project FROM actions_component AS ac "
                    "JOIN components_links_var AS clv ON clv.id_act == ac.id "
                    "JOIN components_links AS cl ON cl.id == clv.id_link "
                    "WHERE ac.id_component_src = ? AND ac.id_project = ? AND cl.id_component_dst == ?", (id_component_src, id_project, id_component_dst,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Action_Component(row[0], row[1], row[2], row[3], row[4], row[5]))

    return result_list

# select all actions by component dest
def select_actions_by_component_and_project_join_link(id_component_src, id_project, id_component_dst):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT ac.id, ac.id_component_src, ac.name, ac.begin_date, ac.edited_date, ac.id_project FROM actions_component AS ac "
                    "JOIN components_links_var AS clv ON clv.id_act = ac.id "
                    "JOIN components_links AS cl ON cl.id = clv.id_link "
                    "WHERE cl.id_component_src = ? AND ac.id_project = ? AND cl.id_component_dst = ?", (id_component_src, id_project, id_component_dst,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Action_Component(row[0], row[1], row[2], row[3], row[4], row[5]))

    return result_list

def select_actions_by_component_project_link(id_component_src, id_project, id_link):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT ac.id, ac.id_component_src, ac.name, ac.begin_date, ac.edited_date, ac.id_project FROM actions_component AS ac "
                    "JOIN components_links_var AS clv ON clv.id_act = ac.id "
                    "WHERE id_component_src = ? AND id_project = ? AND clv.id_link = ?", (id_component_src, id_project, id_link,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Action_Component(row[0], row[1], row[2], row[3], row[4], row[5]))

    return result_list

# select all losses ordering by id_loss
def select_actions_by_component(id_component, id_action):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM actions_component WHERE id_component_src = ? AND id_action = ?", (id_component, id_action))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Action_Component(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    return result_list

# select all losses ordering by id_loss
def select_components_by_action(action, id_project):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM components WHERE id_thing = ? AND id_project = ?", (action.source, id_project,))

        rows = cur.fetchall()

        for row in rows:
            comp = Component(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            list_aux = select_actions_by_component(comp.id, action.id)
            if len(list_aux) > 0:
                result_list.append(Component_Actions(comp, list_aux))

    return result_list

# select all losses ordering by id_loss
def select_id_actions_by_controller(id_controller):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM actions_component WHERE id_component_src = ?", (id_controller,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(row[0])

    return result_list

# select all control actions that are not external from analysis
# def select_actions_not_external_by_project(id_project):
#     result_list = []
#
#     # create a database connection
#     conn = create_connection()
#     with conn:
#         cur = conn.cursor()
#         cur.execute("SELECT ac.id, ac.id_component_src, ac.name, ac.begin_date, ac.edited_date, ac.id_project FROM actions_component AS ac "
#                     "JOIN components AS c ON c.id = ac.id_component_src "
#                     "WHERE ac.id_project = ? AND c.is_external_component = 0", (id_project,))
#
#         rows = cur.fetchall()
#
#         for row in rows:
#             result_list.append(Action_Component(row[0], row[1], row[2], row[3], row[4], row[5]))
#
#     return result_list

def select_name_actions_by_controller(id_controller):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM actions_component WHERE id_component_src = ?", (id_controller,))
        rows = cur.fetchall()

        sql = "SELECT cs.name, cd.name FROM components_links AS cl " \
              "JOIN components AS cs ON cl.id_component_src = cs.id " \
              "JOIN components AS cd ON cl.id_component_dst = cd.id " \
              "JOIN components_links_var AS clv ON clv.id_link = cl.id " \
              "WHERE clv.id_act = ?"

        for row in rows:
            links = ""
            cur.execute(sql, (row[0],))
            rows_links = cur.fetchall()

            for row_l in rows_links:
                links += " (" + row_l[0] + " -> " + row_l[1] + ")"

            result_list.append(row[1] + links)

    return result_list

# def select_name_actions_by_link(id_link):
#     result_list = []
#
#     # create a database connection
#     conn = create_connection()
#     with conn:
#         cur = conn.cursor()
#         cur.execute("SELECT a.name FROM actions_component AS a " \
#              "JOIN components_links_var AS clv ON clv.id_act = a.id " \
#              "WHERE clv.id_link = ?", (id_link,))
#
#         rows = cur.fetchall()
#
#         for row in rows:
#             result_list.append(row[0])
#
#     return result_list


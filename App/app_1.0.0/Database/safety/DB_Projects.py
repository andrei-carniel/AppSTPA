import sqlite3
from sqlite3 import Error

import Constant
from Objects.Project import Project


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
    sql_create_projects_table = "CREATE TABLE IF NOT EXISTS projects(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT, " \
                                "begin_date TEXT NOT NULL, edited_date TEXT" \
                                ");"

    return sql_create_projects_table


# insert one register to Table Projects
def insert_to_projects(project):
    # create a database connection
    conn = create_connection()
    with conn:
        sql = "INSERT INTO projects (name, description, begin_date) VALUES(?, ?, ?)"
        cur = conn.cursor()
        task = (project.name, project.description, project.begin_date)
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid

def delete(id_project):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()

        cur.execute("SELECT id FROM hazards WHERE id_project = ?", (id_project,))
        rows_haz = cur.fetchall()
        for haz_id in rows_haz:
            # delete by other thing
            cur.execute("DELETE FROM hazards_losses WHERE id_hazard = ?", (haz_id[0],))
            # delete safety constraints
            cur.execute("DELETE FROM safety_constraints_hazards WHERE id_hazard = ?", (haz_id[0],))

        # delete by component id
        cur.execute("SELECT id FROM components WHERE id_project = ?", (id_project,))
        rows_comp = cur.fetchall()
        for comp_id in rows_comp:
            # delete var and value
            cur.execute("SELECT id FROM variables WHERE id_component = ?", (comp_id[0],))
            rows_var = cur.fetchall()
            for var_id in rows_var:
                cur.execute("DELETE FROM variables_values WHERE id_variable = ?", (var_id[0],))
                cur.execute("DELETE FROM components_links_var WHERE id_var = ?", (var_id[0],))
                cur.execute("DELETE FROM variables WHERE id = ?", (var_id[0],))

            #  delete component_link
            cur.execute("SELECT id FROM components_links WHERE id_component_src = ? OR id_component_dst = ?",(comp_id[0], comp_id[0],))
            rows_link_var = cur.fetchall()
            for lv in rows_link_var:
                cur.execute("DELETE FROM components_links_var WHERE id_link = ?", (lv[0],))

            cur.execute("DELETE FROM components_links WHERE id_component_src = ? OR id_component_dst = ?",(comp_id[0], comp_id[0],))

            # delete control actions
            cur.execute("SELECT id FROM actions_component WHERE id_project = ?", (id_project,))
            rows_actions = cur.fetchall()
            for act_id in rows_actions:
                cur.execute("SELECT id FROM saf_uca WHERE id_control_action = ?", (act_id[0],))
                rows_uca = cur.fetchall()
                for uca_id in rows_uca:
                    cur.execute("DELETE FROM saf_uca_hazard WHERE id_uca = ?", (uca_id[0],))
                    cur.execute("DELETE FROM saf_uca_context WHERE id_uca = ?", (uca_id[0],))
                    cur.execute("DELETE FROM saf_uca WHERE id = ?", (uca_id[0],))

                cur.execute("DELETE FROM components_links_var WHERE id_act = ?", (act_id[0],))
                cur.execute("DELETE FROM actions_component WHERE id = ?", (act_id[0],))

            cur.execute("DELETE FROM components WHERE id = ?", (comp_id[0],))

        # delete by id project
        cur.execute("DELETE FROM goals WHERE id_project = ?", (id_project,))
        cur.execute("DELETE FROM assumptions WHERE id_project = ?", (id_project,))
        cur.execute("DELETE FROM losses WHERE id_project = ?", (id_project,))
        cur.execute("DELETE FROM hazards WHERE id_project = ?", (id_project,))
        cur.execute("DELETE FROM safety_constraints WHERE id_project = ?", (id_project,))
        cur.execute("DELETE FROM saf_loss_scenario_req WHERE id_project = ?", (id_project,))
        cur.execute("DELETE FROM projects WHERE id = ?", (id_project,))

        conn.commit()
        return cur.lastrowid

# select all projects ordering by name
def select_all_projects():
    """
    Query tasks by all rows
    :return: List of Projects
    """
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM projects ORDER BY name")

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Project(row[0], row[1], row[2], row[3], row[4]))

    return result_list

# select all projects ordering by name
def select_project_by_id(id_project):
    """
    Query tasks by all rows
    :return: List of Projects
    """
    result = None

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM projects WHERE id = ? ORDER BY name", (id_project,))

        row = cur.fetchone()

        if row != None:
            result = Project(row[0], row[1], row[2], row[3], row[4])

    return result

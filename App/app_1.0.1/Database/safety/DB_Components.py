import sqlite3
from sqlite3 import Error

import Constant
from Database.safety import DB_Components_Links, DB_Variables, DB_Actions_Components
from Objects.Component import Component, Component_small


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
    sql_query = "CREATE TABLE components (id INTEGER PRIMARY KEY AUTOINCREMENT, id_thing INTEGER NOT NULL, id_project INTEGER NOT NULL, " \
                "name TEXT NOT NULL, begin_date TEXT NOT NULL, edited_date TEXT, comp_father INTEGER NOT NULL DEFAULT 0, " \
                "is_external_component INTEGER NOT NULL DEFAULT 0, hlc_control INTEGER NOT NULL DEFAULT 0, is_human INTEGER NOT NULL DEFAULT 0, " \
                "FOREIGN KEY(id_thing) REFERENCES things(id) " \
                "FOREIGN KEY(id_project) REFERENCES projects(id))"

    return sql_query

# insert one register to Table Components
def insert_controller(comp):
    # create a database connection
    conn = create_connection()
    with conn:
        sql = "INSERT INTO components(id_thing, id_project, name, begin_date, is_external_component, is_human) VALUES(?, ?, ?, ?, ?, ?)"
        cur = conn.cursor()
        task = (comp.id_thing, comp.id_project, comp.name, comp.begin_date, comp.is_external_component, comp.is_human)
        cur.execute(sql, task)

        id_c = cur.lastrowid
        sql_son = "INSERT INTO components(id_thing, id_project, name, begin_date, comp_father, is_external_component) VALUES(?, ?, ?, ?, ?, ?)"
        alg = comp.name + " " + Constant.ALGORITHM + "/Logic"
        cur.execute(sql_son, (Constant.DB_ID_ALGORITHM, comp.id_project, alg, comp.begin_date, id_c, comp.is_external_component, ))

        pm = comp.name + " Process Model"
        cur.execute(sql_son, (Constant.DB_ID_PROCESS_MODEL, comp.id_project, pm, comp.begin_date, id_c, comp.is_external_component))

        conn.commit()
        return cur.lastrowid# insert one register to Table Components

# NOT USED
# def insert_controller_ext_system(id_project, id_controller, name_controller):
#     # create a database connection
#     now = datetime.now()
#     begin_date = now.strftime(Constant.DATETIME_MASK)
#
#     conn = create_connection()
#     with conn:
#         cur = conn.cursor()
#         ei = name_controller + " External Information"
#         sql_son = "INSERT INTO components(id_thing, id_project, name, begin_date, comp_father) VALUES(?, ?, ?, ?, ?)"
#         cur.execute(sql_son, (Constant.DB_ID_EXT_INFORMATION, id_project, ei, begin_date, id_controller,))
#         id_ei = cur.lastrowid
#
#         sql_link = "INSERT INTO components_links(id_component_src, id_component_dst) VALUES(?, ?)"
#         cur.execute(sql_link, (id_ei, id_controller,))  # IN
#         # cur.execute(sql_link, (id_controller, id_ei,))  # OUT
#
#         conn.commit()
#         return cur.lastrowid

def insert_controlled_process(comp):
    # create a database connection
    conn = create_connection()
    with conn:
        sql = "INSERT INTO components(id_thing, id_project, name, begin_date) VALUES(?, ?, ?, ?)"
        cur = conn.cursor()
        task = (comp.id_thing, comp.id_project, comp.name, comp.begin_date)
        cur.execute(sql, task)
        id_c = cur.lastrowid

        sql_son = "INSERT INTO components(id_thing, id_project, name, begin_date, comp_father) VALUES(?, ?, ?, ?, ?)"
        inp = comp.name + " " + Constant.INPUT
        cur.execute(sql_son, (Constant.DB_ID_INPUT, comp.id_project, inp, comp.begin_date, id_c,))
        id_in = cur.lastrowid

        out = comp.name + " " + Constant.OUTPUT
        cur.execute(sql_son, (Constant.DB_ID_OUTPUT, comp.id_project, out, comp.begin_date, id_c,))
        id_out = cur.lastrowid

        env = comp.name + " " + Constant.ENVIRONMENTAL_DISTURBANCES
        cur.execute(sql_son, (Constant.DB_ID_ENV_DISTURBANCES, comp.id_project, env, comp.begin_date, id_c,))
        id_env = cur.lastrowid

        # sql_link = "INSERT INTO components_links(id_component_src, id_component_dst) VALUES(?, ?)"
        # cur.execute(sql_link, (id_in, id_c,))
        # id_link_in_cp = cur.lastrowid
        # cur.execute(sql_link, (id_c, id_out,))
        # id_link_cp_out = cur.lastrowid

        sql_var = "INSERT INTO variables (id_component, id_project, name, begin_date) VALUES(?, ?, ?, ?)"
        cur.execute(sql_var, (id_in, comp.id_project, Constant.INPUT, comp.begin_date,))
        cur.execute(sql_var, (id_out, comp.id_project, Constant.OUTPUT, comp.begin_date,))
        cur.execute(sql_var, (id_env, comp.id_project, Constant.ENVIRONMENTAL_DISTURBANCES, comp.begin_date,))

        conn.commit()
        return cur.lastrowid

def insert_to_table(comp):
    # create a database connection
    conn = create_connection()
    with conn:
        sql = "INSERT INTO components(id_thing, id_project, name, begin_date) VALUES(?, ?, ?, ?)"
        cur = conn.cursor()
        task = (comp.id_thing, comp.id_project, comp.name, comp.begin_date)
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid

# update one register to Table Goals
def update_component(comp):
    # create a database connection
    conn = create_connection()
    with conn:
        sql = "UPDATE components SET name = ?, edited_date = ? WHERE id = ?"
        cur = conn.cursor()
        task = (comp.name, comp.edited_date, comp.id)
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid

def update_component_dfd(id_comp, name_dfd):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM sec_stride_dfd WHERE name = ?", (name_dfd,))
        row_dfd = cur.fetchone()

        if row_dfd != None:
            sql = "UPDATE components SET id_stride_dfd = ? WHERE id = ?"
            task = (row_dfd[0], id_comp)
            cur.execute(sql, task)
            conn.commit()
            return cur.lastrowid
        return -1

# update one register to Table Goals
def update_component_controller(comp):
    # create a database connection
    conn = create_connection()
    with conn:
        sql = "UPDATE components SET name = ?, edited_date = ?, is_external_component = ?, is_human = ? WHERE id = ?"
        cur = conn.cursor()
        task = (comp.name, comp.edited_date, comp.is_external_component, comp.is_human, comp.id)
        cur.execute(sql, task)

        sql_son = "UPDATE components SET name = ?, edited_date = ?, is_external_component = ?, is_human = ? WHERE comp_father = ? AND id_thing = ?"

        alg = comp.name + " " + Constant.ALGORITHM + "/Logic"
        cur.execute(sql_son, (alg, comp.edited_date, comp.is_external_component, comp.is_human, comp.id, Constant.DB_ID_ALGORITHM,))

        pm = comp.name + " Process Model"
        cur.execute(sql_son, (pm, comp.edited_date, comp.is_external_component, comp.is_human, comp.id, Constant.DB_ID_PROCESS_MODEL,))

        # ei = comp.name + " External Information"
        # cur.execute(sql_son, (ei, comp.edited_date, comp.is_external_component, comp.id, Constant.DB_ID_EXT_INFORMATION,))

        conn.commit()
        return cur.lastrowid

def delete(comp):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM components WHERE id = ?", (comp.id,))
        conn.commit()
        DB_Components_Links.delete_by_src_dst(comp.id)
        return cur.lastrowid

def delete_controller(comp):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM components WHERE id = ?", (comp.id,))
        cur.execute("DELETE FROM components WHERE comp_father = ?", (comp.id,))
        conn.commit()
        DB_Actions_Components.delete_by_controller(comp.id)
        DB_Variables.delete_by_component(comp.id)
        DB_Components_Links.delete_by_src_dst(comp.id)
        return cur.lastrowid

def delete_controller_ext_comp(ext_id):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM components WHERE id = ?", (ext_id,))
        conn.commit()
        DB_Actions_Components.delete_by_controller(ext_id)
        DB_Variables.delete_by_component(ext_id)
        DB_Components_Links.delete_by_src_dst(ext_id)
        return cur.lastrowid

def delete_controlled_procces(comp):
    # create a database connection
    conn = create_connection()
    with conn:
        list_comp = select_component_by_father(comp.id)

        cur = conn.cursor()
        cur.execute("DELETE FROM components WHERE id = ?", (comp.id,))
        cur.execute("DELETE FROM components WHERE comp_father = ?", (comp.id,))
        conn.commit()
        DB_Variables.delete_by_component(comp.id)
        DB_Components_Links.delete_by_src_dst(comp.id)

        for c in list_comp:
            DB_Variables.delete_by_component(c.id)

        return cur.lastrowid

# select all withou order
def select_all_components_by_project_analysis(id_project):
    """
    Query tasks by all rows
    :return: List of Losses
    """
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT c.id, c.id_thing, c.id_project, c.name, c.begin_date, c.edited_date, c.comp_father, c.is_external_component, c.hlc_control, t.ontology_name "
                    "FROM components AS c "
                    "JOIN things AS t ON t.id = c.id_thing "
                    "WHERE c.id_project = ?", (id_project,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))

    return result_list

# select all withou order
def select_all_components_by_project_analysis_order_by_name(id_project):
    """
    Query tasks by all rows
    :return: List of Losses
    """
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT c.id, c.id_thing, c.id_project, c.name, c.begin_date, c.edited_date, c.comp_father, c.is_external_component, c.hlc_control, t.ontology_name "
                    "FROM components AS c "
                    "JOIN things AS t ON t.id = c.id_thing "
                    "WHERE c.id_project = ? AND c.id_thing <> 8 AND c.id_thing <> 9  AND c.id_thing <> 10 "
                    "ORDER BY c.name", (id_project,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))

    return result_list

# select component by id thing
def select_controller_not_external_project_analysis(id_project):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM components WHERE id_thing = ? AND id_project = ? AND is_external_component = 0", (Constant.DB_ID_CONTROLLER, id_project,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

    return result_list

def select_controller_not_external_not_human(id_project):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM components WHERE id_thing = ? AND id_project = ? AND is_external_component = 0 AND is_human = 0", (Constant.DB_ID_CONTROLLER, id_project,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

    return result_list

def select_performance_component_not_external_not_human(id_project):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        sql = "SELECT * FROM components WHERE id_project = ? AND is_external_component = 0 AND is_human = 0 AND (id_thing = ? OR id_thing = ? OR id_thing = ?)"
        cur.execute(sql, (id_project, Constant.DB_ID_CONTROLLER, Constant.DB_ID_ALGORITHM, Constant.DB_ID_PROCESS_MODEL))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

    return result_list

# select component by id thing
def select_component_by_thing_project_analysis(id_thing, id_project):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT id, id_thing, id_project, name, begin_date, edited_date, comp_father, is_external_component, hlc_control, is_human "
                    "FROM components WHERE id_thing = ? AND id_project = ? ", (id_thing, id_project,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], "", row[9]))

    return result_list

# select component by id thing
def select_component_by_thing_project_analysis_except(id_thing, id_project, id_except):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM components WHERE id_thing = ? AND id_project = ? AND id <> ?", (id_thing, id_project, id_except,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

    return result_list

# select component by id thing
def select_component_by_project_father_thing(id_project, id_father, id_thing):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM components WHERE id_project = ? AND comp_father = ? AND id_thing = ? ", (id_project, id_father, id_thing,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

    return result_list

# select component by id thing
def select_component_by_father(id_father):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM components WHERE comp_father = ?", (id_father,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

    return result_list

# select component by id thing
def select_one_component_by_thing_project_analysis(id_thing, id_project):
    result = None

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM components WHERE id_thing = ? AND id_project = ? ", (id_thing, id_project,))

        row = cur.fetchone()

        if row != None:
            result = Component(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])

    return result

# select component by id thing
def select_component_by_name_thing_project_analysis(name_thing, id_project):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT c.id, c.id_thing, c.id_project, c.name, c.begin_date, c.edited_date, c.comp_father, c.is_external_component, c.hlc_control, t.ontology_name "
                    "FROM components AS c "
                    "JOIN things AS t ON t.id = c.id_thing "
                    "WHERE t.ontology_name = ? AND c.id_project = ? ", (name_thing, id_project,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))

    return result_list

# select component by id thing
def select_component_by_id(id_controller):
    result = None

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM components WHERE id = ?", (id_controller,))

        row = cur.fetchone()

        if row != None:
            result = Component(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])

    return result

# select links for controller
def select_components_to_link_with_controller(id_project, id_controller, list_of_things):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()

        things_text = ""
        for t in list_of_things:
            if things_text != "":
                things_text += " OR "
            things_text += "id_thing = " + str(t)

        sqlquery = "SELECT * FROM components WHERE id_project = ? AND id <> ?"

        if len(things_text) > 0:
            sqlquery += " AND (" + things_text + ")"

        # sqlquery += " AND (comp_father = 0 OR comp_father = ?)"

        cur.execute(sqlquery, (id_project, id_controller,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

    return result_list

# select links for actuator
def select_components_to_link_with_actuator(id_project, id_actuator, list_of_things):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()

        things_text = ""
        for t in list_of_things:
            if things_text != "":
                things_text += " OR "
            things_text += "id_thing = " + str(t)

        sqlquery = "SELECT * FROM components WHERE id_project = ? AND id <> ?"

        if len(things_text) > 0:
            sqlquery += " AND (" + things_text + ")"


        cur.execute(sqlquery, (id_project, id_actuator,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

    return result_list

# select links for controlled process
def select_components_to_link_with_cp(id_project, id_cp, list_of_things):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()

        things_text = ""
        for t in list_of_things:
            if things_text != "":
                things_text += " OR "
            things_text += "id_thing = " + str(t)

        sqlquery = "SELECT * FROM components WHERE id_project = ? AND id <> ?"

        if len(things_text) > 0:
            sqlquery += " AND (" + things_text + ")"

        cur.execute(sqlquery, (id_project, id_cp,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

    return result_list

# select links for actuator
def select_components_to_link_with_sensor(id_project, id_sensor, list_of_things):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()

        things_text = ""
        for t in list_of_things:
            if things_text != "":
                things_text += " OR "
            things_text += "id_thing = " + str(t)

        sqlquery = "SELECT * FROM components WHERE id_project = ? AND id <> ?"

        if len(things_text) > 0:
            sqlquery += " AND (" + things_text + ")"

        cur.execute(sqlquery, (id_project, id_sensor,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

    return result_list

# select controllers except
def select_component_by_thing_project_exceptId(id_thing, id_project, id_except):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM components WHERE id_thing = ? AND id_project = ? AND id <> ? ", (id_thing, id_project, id_except,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

    return result_list

def select_controlled_process_values(id_project, id_father, id_thing):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT val.value FROM components AS c "
                    "JOIN variables AS v ON v.id_component = c.id "
                    "JOIN variables_values as val ON val.id_variable = v.id "
                    "WHERE c.id_project = ? AND c.comp_father = ? AND c.id_thing = ?", (id_project, id_father, id_thing,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(row[0])

    return result_list

def delete_report(id_controller):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT count(id) FROM actions_component WHERE id_component_src = ?", (id_controller,))
        row = cur.fetchone()
        if row != None:
            if row[0] > 0:
                result_list.append("Control Actions: " + str(row[0]))

        cur.execute("SELECT count(id) FROM variables WHERE id_component = ?", (id_controller,))
        row = cur.fetchone()
        if row != None:
            if row[0] > 0:
                result_list.append("Variables: " + str(row[0]))

        cur.execute("SELECT count(id) FROM components_links WHERE id_component_src = ? OR id_component_dst = ?", (id_controller, id_controller,))
        row = cur.fetchone()
        if row != None:
            if row[0] > 0:
                result_list.append("Connections: " + str(row[0]))


        cur.execute("SELECT count(id) FROM saf_uca WHERE id_controller = ? AND is_hazardous = 1", (id_controller,))
        row = cur.fetchone()
        if row != None:
            if row[0] > 0:
                result_list.append("Unsafe Control Actions: " + str(row[0]))


        cur.execute("SELECT count(id) FROM saf_loss_scenario_req WHERE id_controller = ?", (id_controller,))
        row = cur.fetchone()
        if row != None:
            if row[0] > 0:
                result_list.append("Recommendations: " + str(row[0]))


    return result_list

def find_component_warnings(id_project):
    result = ""

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        # incoming
        cur.execute("SELECT c.name, t.name FROM components AS c "
                    "LEFT JOIN components_links AS cl ON cl.id_component_dst = c.id "
                    "JOIN things AS t On t.id = c.id_thing "
                    "WHERE cl.id_component_dst IS NULL AND c.id_thing != 5 AND c.id_thing != 6 AND c.id_thing != 8 AND c.id_thing != 9 AND c.id_thing != 10  AND c.id_project = ?",
                    (id_project,))

        row_incoming = cur.fetchall()
        result_in = ""
        for row in row_incoming:
            if result_in == "":
                result_in += "No incoming connections\n"
            result_in += "\t" + row[0] + " (" + row[1] + ")\n"

        # outgoing
        cur.execute("SELECT c.name, t.name FROM components AS c "
                    "LEFT JOIN components_links AS cl ON cl.id_component_src = c.id "
                    "JOIN things AS t On t.id = c.id_thing "
                    "WHERE cl.id_component_src IS NULL AND c.id_thing != 5 AND c.id_thing != 6 AND c.id_thing != 8 AND c.id_thing != 9 AND c.id_thing != 10  AND c.id_project = ?",
                    (id_project,))

        row_outgoing = cur.fetchall()
        result_out = ""
        for row in row_outgoing:
            if result_out == "":
                result_out += "No outgoing connections\n"
            result_out += "\t" + row[0] + " (" + row[1] + ")\n"


        # no control action
        cur.execute("SELECT c.name FROM components AS c "
                    "LEFT JOIN actions_component AS ac ON c.id = ac.id_component_src "
                    "WHERE ac.id_component_src IS NULL AND c.id_thing = 1 AND c.id_project = ?",
                    (id_project,))

        row_act = cur.fetchall()
        result_act = ""
        for row in row_act:
            if result_act == "":
                result_act += "Controller(s) without control action\n"
            result_act += "\t" + row[0] + "\n"

        # no feedback
        cur.execute("SELECT c.name FROM components AS c "
                    "LEFT JOIN variables AS v ON c.id = v.id_component "
                    "WHERE v.id_component IS NULL AND c.id_thing = 1 AND c.id_project = ?",
                    (id_project,))

        row_feed = cur.fetchall()
        result_feed = ""
        for row in row_feed:
            if result_feed == "":
                result_feed += "Controller(s) without feedback\n"
            result_feed += "\t" + row[0] + "\n"


        result = result_in

        if result != "" and result_out != "":
            result += "\n"
        result += result_out

        if result != "" and result_act != "":
            result += "\n"
        result += result_act

        if result != "" and result_feed != "":
            result += "\n"
        result += result_feed

    return result

def select_dfd_elements(id_project):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        sql = "SELECT id, id_thing, name, id_stride_dfd FROM components " \
                    "WHERE id_project = ? " \
                    "AND id_thing != " + str(Constant.DB_ID_INPUT) +\
                    " AND id_thing != " + str(Constant.DB_ID_OUTPUT) +\
                    " AND id_thing != " + str(Constant.DB_ID_EXT_INFORMATION) +\
                    " AND id_thing != " + str(Constant.DB_ID_ALGORITHM) +\
                    " AND id_thing != " + str(Constant.DB_ID_PROCESS_MODEL) +\
                    " AND id_thing != " + str(Constant.DB_ID_ENV_DISTURBANCES) +\
                    " AND is_human = 0"
        cur.execute(sql, (id_project,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component_small(row[0], row[1], row[2], row[3]))


    return result_list
import sqlite3
from sqlite3 import Error

import Constant
from Objects.Component import Component_Link, Component_Link_Var, Component_Link_Onto, Component_Link_Var_HLC, \
    Component_Link_Ext, Component_Link_Stride
from Objects.Goal import Goal


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
    sql_create_goals_table = "CREATE TABLE components_links (id INTEGER PRIMARY KEY AUTOINCREMENT, id_component_src INTEGER NOT NULL, " \
                             "id_component_dst INTEGER NOT NULL, is_bound_trust INTEGER NOT NULL DEFAULT 0, " \
                             "id_stride_dfd INTEGER REFERENCES sec_stride_dfd(id), " \
                             "FOREIGN KEY(id_component_src) REFERENCES components(id) " \
                             "FOREIGN KEY(id_component_dst) REFERENCES components(id))"

    return sql_create_goals_table

def create_table_component_link_var():
    sql_create_goals_table = "CREATE TABLE IF NOT EXISTS components_links_var (id INTEGER PRIMARY KEY, id_link INTEGER NOT NULL, id_var INTEGER, id_act INTEGER, " \
                             "FOREIGN KEY(id_link) REFERENCES components_links(id) " \
                             "FOREIGN KEY(id_var) REFERENCES variables(id) " \
                             "FOREIGN KEY(id_act) REFERENCES actions_component(id))"

    return sql_create_goals_table

# insert one register to Table Goals
def insert(src, dest):
    # create a database connection
    conn = create_connection()
    with conn:
        sql = "INSERT INTO components_links(id_component_src, id_component_dst, id_stride_dfd) VALUES(?, ?, ?)"
        cur = conn.cursor()
        task = (src, dest, Constant.DB_ID_DATA_FLOW)
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid

def delete(link):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM components_links_var WHERE id_link = ?", (link.id,))
        cur.execute("DELETE FROM components_links WHERE id = ?", (link.id,))
        conn.commit()
        return cur.lastrowid

def delete_by_src_dst(id_comp):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM components_links WHERE id_component_src = ? OR id_component_dst = ?", (id_comp, id_comp,))
        rows_link_var = cur.fetchall()
        for lv in rows_link_var:
            cur.execute("DELETE FROM components_links_var WHERE id_link = ?", (lv[0],))

        cur.execute("DELETE FROM components_links WHERE id_component_src = ? OR id_component_dst = ?", (id_comp, id_comp,))
        conn.commit()
        return cur.lastrowid

def update(id_link, is_bound_trust):
    # create a database connection
    conn = create_connection()
    with conn:
        sql = "UPDATE components_links SET is_bound_trust = ? WHERE id = ?"
        cur = conn.cursor()
        task = (is_bound_trust, id_link)
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid

# select links by source
def get_by_id(id):
    result_list = None

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        sqlquery = "SELECT DISTINCT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name " \
                   "FROM components_links AS cl " \
                   "JOIN components AS cs ON cl.id_component_src = cs.id " \
                   "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                   "JOIN components_links_var AS clv ON clv.id_link = cl.id " \
                   "WHERE cl.id = ?"
        cur.execute(sqlquery, (id,))

        row = cur.fetchone()
        if row != None:
            result_list = Component_Link(row[0], row[1], row[2], row[3], row[4])

    return result_list

# select links by source
def select_component_links_by_project_and_thing(id_project, id_thing, find_for_source):
    """
    Query tasks by all rows
    :return: List of Goals
    """
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()

        sqlquery = "SELECT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name " \
                    "FROM components_links AS cl " \
                    "JOIN components AS cs ON cl.id_component_src = cs.id " \
                    "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                    "WHERE cs.id_project = ? AND cd.id_project = ?"

        if find_for_source:
            sqlquery += " AND cs.id_thing = ?"
        else:
            sqlquery += " AND cd.id_thing = ?"


        cur.execute(sqlquery, (id_project, id_project, id_thing,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component_Link(row[0], row[1], row[2], row[3], row[4]))

    return result_list

def select_component_links_by_project_and_thing_and_controller(id_project, id_thing, id_controller, controller_is_source):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()

        sqlquery = "SELECT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name FROM components_links AS cl " \
                   "JOIN components AS cs ON cl.id_component_src = cs.id " \
                   "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                   "WHERE cs.id_project = ? AND cd.id_project = ? "

        if controller_is_source:
            sqlquery += " AND cd.id_thing = ? AND cl.id_component_src = ?"
        else:
            sqlquery += " AND cs.id_thing = ? AND cl.id_component_dst =  ?"

        cur.execute(sqlquery, (id_project, id_project, id_thing, id_controller,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component_Link(row[0], row[1], row[2], row[3], row[4]))

    return result_list

def select_component_links_by_project_and_thing_and_controller_CA_ONLY(id_project, id_thing, id_controller, controller_is_source):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()

        sqlquery = "SELECT DISTINCT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name FROM components_links AS cl " \
                   "JOIN components_links_var AS clv ON cl.id = clv.id_link " \
                   "JOIN components AS cs ON cl.id_component_src = cs.id " \
                   "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                   "WHERE clv.id_act > 0 AND cs.id_project = ? AND cd.id_project = ? "

        if controller_is_source:
            sqlquery += " AND cd.id_thing = ? AND cl.id_component_src = ?"
        else:
            sqlquery += " AND cs.id_thing = ? AND cl.id_component_dst =  ?"

        cur.execute(sqlquery, (id_project, id_project, id_thing, id_controller,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component_Link(row[0], row[1], row[2], row[3], row[4]))

    return result_list

# select links by source or destiny
def select_component_links_by_project_and_component(id_component, find_for_source):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()

        sqlquery = "SELECT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name FROM components_links AS cl " \
                   "JOIN components AS cs ON cl.id_component_src = cs.id " \
                   "JOIN components AS cd ON cl.id_component_dst = cd.id "

        if find_for_source:
            sqlquery += " WHERE cl.id_component_src = ?"
        else:
            sqlquery += " WHERE cl.id_component_dst = ?"


        cur.execute(sqlquery, (id_component,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component_Link(row[0], row[1], row[2], row[3], row[4]))

    return result_list

# select links by source
def select_all_component_links_feedback_by_component(id_component):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()

        # flow to controller
        sqlquery = "SELECT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name FROM components_links AS cl " \
                   "JOIN components AS cs ON cl.id_component_src = cs.id " \
                   "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                   "WHERE cl.id_component_dst = ?"

        cur.execute(sqlquery, (id_component,))
        rows = cur.fetchall()
        for row in rows:
            result_list.append(Component_Link(row[0], row[1], row[2], row[3], row[4]))

        sqlquery = "SELECT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name FROM components_links AS cl " \
                   "JOIN components AS cs ON cl.id_component_src = cs.id " \
                   "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                   "WHERE cl.id_component_src = ? AND cd.id_thing = ?"

        cur.execute(sqlquery, (id_component, Constant.DB_ID_EXT_INFORMATION))
        rows = cur.fetchall()
        for row in rows:
            result_list.append(Component_Link(row[0], row[1], row[2], row[3], row[4]))

    return result_list

def select_all_component_links_actions_by_component(id_component):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()

        sqlquery = "SELECT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name FROM components_links AS cl " \
                   "JOIN components AS cs ON cl.id_component_src = cs.id " \
                   "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                   "WHERE cl.id_component_src = ? AND cs.id_thing == 1"

        cur.execute(sqlquery, (id_component,))
        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component_Link(row[0], row[1], row[2], row[3], row[4]))

    return result_list

def select_all_control_actions_in_link(list_links):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()

        sqlquery = "SELECT ac.name, cs.name, cd.name FROM components_links AS cl " \
                   "JOIN components_links_var AS clv ON clv.id_link = cl.id " \
                   "JOIN actions_component AS ac ON ac.id = clv.id_act " \
                   "JOIN components AS cs ON cl.id_component_src = cs.id " \
                   "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                   "WHERE cl.id_component_src = ? AND cl.id_component_dst = ? AND clv.id_act > 0 AND cs.id_thing = 1"

        for link in list_links:
            cur.execute(sqlquery, (link.id_component_dst, link.id_component_src,))
            rows = cur.fetchall()

            for row in rows:
                result_list.append("The " + row[1] + " sends the control action \"" + row[0] + "\" in the link: " + row[1] + " -> " + row[2])

    return result_list

def select_all_component_links_onto_name_by_project(id_project):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()

        sqlquery = "SELECT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name, ts.ontology_name, td.ontology_name FROM components_links AS cl " \
                   "JOIN components AS cs ON cl.id_component_src = cs.id " \
                   "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                   "JOIN things AS ts ON ts.id = cs.id_thing " \
                   "JOIN things AS td ON td.id = cd.id_thing " \
                   "WHERE cs.id_project = ? AND cd.id_project = ?"

        cur.execute(sqlquery, (id_project, id_project,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component_Link_Onto(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    return result_list

# select links by source
def select_var_link(id_var):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()

        sqlquery = "SELECT * FROM components_links_var WHERE id_var = ?"


        cur.execute(sqlquery, (id_var,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component_Link_Var(row[0], row[1], row[2], row[3]))

    return result_list

# select links by source
def select_act_link(id_act):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()

        sqlquery = "SELECT * FROM components_links_var WHERE id_act = ?"

        cur.execute(sqlquery, (id_act,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component_Link_Var(row[0], row[1], row[2], row[3]))

    return result_list

# select control actions of hlc to controller
def select_act_by_controller_hlc(id_controller, list_id_hlc):
    result_list = []
    control_actions = ""

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()

        sqlquery = "SELECT clv.id, ac.name FROM components_links AS cl " \
                   "JOIN components_links_var AS clv ON clv.id_link = cl.id " \
                   "JOIN actions_component AS ac ON ac.id = clv.id_act " \
                   "WHERE cl.id_component_src = ? AND cl.id_component_dst = ? AND clv.id_act > 0"

        for id_hlc in list_id_hlc:
            cur.execute(sqlquery, (id_controller, id_hlc,))
            rows = cur.fetchall()

            for row in rows:
                result_list.append(row[0])
                if control_actions != "":
                    control_actions += "\n- "
                else:
                    control_actions += "- "

                control_actions += row[1]

    return result_list, control_actions

# select feed of controller to hlc
def select_feed_by_controller_hlc(id_controller, list_id_hlc):
    result_list = []
    feedback = ""

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()

        sqlquery = "SELECT clv.id, v.name FROM components_links AS cl " \
                   "JOIN components_links_var AS clv ON clv.id_link = cl.id " \
                   "JOIN variables as v ON v.id = clv.id_var " \
                   "WHERE cl.id_component_src = ? AND cl.id_component_dst = ? AND clv.id_var > 0"

        for id_hlc in list_id_hlc:
            cur.execute(sqlquery, (id_hlc, id_controller, ))
            rows = cur.fetchall()

            for row in rows:
                result_list.append(row[0])
                if feedback != "":
                    feedback += "\n- "
                else:
                    feedback += "- "

                feedback += row[1]

    return result_list, feedback

def delete_link_var(id_var):
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM components_links_var WHERE id_var = ?", (id_var,))
        conn.commit()
        return cur.lastrowid

def delete_link_act(id_act):
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM components_links_var WHERE id_act = ?", (id_act,))
        conn.commit()
        return cur.lastrowid

def insert_link_var(id_var, id_link):
    # create a database connection
    conn = create_connection()
    with conn:
        sql = "INSERT INTO components_links_var (id_link, id_var) VALUES(?, ?)"
        cur = conn.cursor()
        task = (id_link, id_var)
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid

def insert_link_act(id_act, id_link):
    # create a database connection
    conn = create_connection()
    with conn:
        sql = "INSERT INTO components_links_var (id_link, id_act) VALUES(?, ?)"
        cur = conn.cursor()
        task = (id_link, id_act)
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid

def select_all_control_action_from_hlc_project(id_project, id_controller_dest):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()

        sqlquery = "SELECT cv.id, cv. id_link, cv.id_var, cv.id_act, ac.name, cl.id_component_src, cl.id_component_dst, cs.name, cd.name " \
                    "FROM components_links_var AS cv " \
                    "JOIN components_links AS cl ON cv.id_link = cl.id " \
		            "JOIN components AS cs ON cl.id_component_src = cs.id " \
		            "JOIN components AS cd ON cl.id_component_dst = cd.id " \
		            "JOIN actions_component AS ac ON cv.id_act = ac.id " \
		            "WHERE cs.id_project = ? AND cd.id_project = ? AND cd.id = ? AND cv.id_act > 0 AND cs.id_thing = 1 AND cd.id_thing = 1"

        cur.execute(sqlquery, (id_project, id_project, id_controller_dest))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component_Link_Var_HLC(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

    return result_list

def select_all_control_actions_by_ID(id_act):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()

        sqlquery = "SELECT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cs.id_thing, cd.name, cd.id_thing FROM components_links AS cl " \
                   "JOIN components AS cs ON cl.id_component_src = cs.id " \
                   "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                   "JOIN components_links_var AS clv ON clv.id_link = cl.id " \
                   "WHERE clv.id_act = ?"

        cur.execute(sqlquery, (id_act,))
        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component_Link_Ext(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    return result_list

def select_all_feedback_by_ID(id_feedback):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()

        sqlquery = "SELECT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cs.id_thing, cd.name, cd.id_thing FROM components_links AS cl " \
                   "JOIN components AS cs ON cl.id_component_src = cs.id " \
                   "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                   "JOIN components_links_var AS clv ON clv.id_link = cl.id " \
                   "WHERE clv.id_var = ?"

        cur.execute(sqlquery, (id_feedback,))
        rows = cur.fetchall()

        for row in rows:
            result_list.append(Component_Link_Ext(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    return result_list

def select_links_stride(id_controller):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()

        sql_right = "SELECT DISTINCT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name, cs.id_thing, cd.id_thing, cl.is_bound_trust, " \
                     "cs.id_stride_dfd, cd.id_stride_dfd, cl.id_stride_dfd FROM components_links AS cl " \
                       "JOIN components AS cs ON cl.id_component_src = cs.id " \
                       "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                       "JOIN components_links_var AS clv ON clv.id_link = cl.id " \
                       "WHERE cl.id_component_dst = ? AND clv.id_var > 0 AND cs.id_thing <> ?"

        sql_to_hlc = "SELECT DISTINCT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name, cs.id_thing, cd.id_thing, cl.is_bound_trust, " \
                     "cs.id_stride_dfd, cd.id_stride_dfd, cl.id_stride_dfd FROM components_links AS cl " \
                     "JOIN components AS cs ON cl.id_component_src = cs.id " \
                     "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                     "JOIN components_links_var AS clv ON clv.id_link = cl.id " \
                     "WHERE cl.id_component_dst = ? AND clv.id_var > 0 AND cs.id_thing == ?"

        sql_to_ext_feed = "SELECT DISTINCT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name, cs.id_thing, cd.id_thing, cl.is_bound_trust, " \
                          "cs.id_stride_dfd, cd.id_stride_dfd, cl.id_stride_dfd FROM components_links AS cl " \
                          "JOIN components AS cs ON cl.id_component_src = cs.id " \
                          "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                          "JOIN components_links_var AS clv ON clv.id_link = cl.id " \
                          "WHERE cl.id_component_src = ? AND cd.id_thing = ?"

        sql_left = "SELECT DISTINCT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name, cs.id_thing, cd.id_thing, cl.is_bound_trust, " \
                   "cs.id_stride_dfd, cd.id_stride_dfd, cl.id_stride_dfd FROM components_links AS cl " \
                   "JOIN components AS cs ON cl.id_component_src = cs.id " \
                   "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                   "JOIN components_links_var AS clv ON clv.id_link = cl.id " \
                   "WHERE cl.id_component_src = ? AND clv.id_act > 0 AND cd.id_thing <> ?"

        sql_left_hlc = "SELECT DISTINCT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name, cs.id_thing, cd.id_thing, cl.is_bound_trust, " \
                       "cs.id_stride_dfd, cd.id_stride_dfd, cl.id_stride_dfd FROM components_links AS cl " \
                       "JOIN components AS cs ON cl.id_component_src = cs.id " \
                       "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                       "JOIN components_links_var AS clv ON clv.id_link = cl.id " \
                       "WHERE cl.id_component_src = ? AND clv.id_act > 0 AND cd.id_thing == ?"
        # get CP and Sensor
        # cur.execute(sql_normal, (Constant.DB_ID_CP, Constant.DB_ID_SENSOR, id_project, id_project,))
        # rows_link_a = cur.fetchall()
        # result_list = construct_stride_object(cur, rows_link_a, False, False)

        # get normal connection to controller
        cur.execute(sql_right, (id_controller, Constant.DB_ID_CONTROLLER,))
        rows_link_a = cur.fetchall()
        result_list = construct_stride_feed_object(cur, rows_link_a, False)

        # get normal connection to hlc
        cur.execute(sql_to_hlc, (id_controller, Constant.DB_ID_CONTROLLER,))
        rows_link_b = cur.fetchall()
        result_list.extend(construct_stride_feed_object(cur, rows_link_b, True))

        # get feedback controller to EXT
        cur.execute(sql_to_ext_feed, (id_controller, Constant.DB_ID_EXT_INFORMATION,))
        rows_link_c = cur.fetchall()
        result_list.extend(construct_stride_feed_object(cur, rows_link_c, False))

        # get normal connection to controller
        cur.execute(sql_left, (id_controller, Constant.DB_ID_CONTROLLER,))
        rows_link_d = cur.fetchall()
        result_list.extend(construct_stride_act_object(cur, rows_link_d, False))

        # get normal connection to hlc
        cur.execute(sql_left_hlc, (id_controller, Constant.DB_ID_CONTROLLER,))
        rows_link_e = cur.fetchall()
        result_list.extend(construct_stride_act_object(cur, rows_link_e, True))

    return result_list

def select_dfd_links(id_project):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        sql_right = "SELECT DISTINCT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name, cs.id_thing, cd.id_thing, cl.is_bound_trust, " \
                    "cs.id_stride_dfd, cd.id_stride_dfd, cl.id_stride_dfd FROM components_links AS cl " \
                    "JOIN components AS cs ON cl.id_component_src = cs.id " \
                    "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                    "JOIN components_links_var AS clv ON clv.id_link = cl.id " \
                    "WHERE cl.id_component_dst = ? AND clv.id_var > 0 AND cs.id_thing <> ?"

        sql_to_hlc = "SELECT DISTINCT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name, cs.id_thing, cd.id_thing, cl.is_bound_trust, " \
                     "cs.id_stride_dfd, cd.id_stride_dfd, cl.id_stride_dfd FROM components_links AS cl " \
                     "JOIN components AS cs ON cl.id_component_src = cs.id " \
                     "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                     "JOIN components_links_var AS clv ON clv.id_link = cl.id " \
                     "WHERE cl.id_component_dst = ? AND clv.id_var > 0 AND cs.id_thing == ?"

        sql_to_ext_feed = "SELECT DISTINCT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name, cs.id_thing, cd.id_thing, cl.is_bound_trust, " \
                          "cs.id_stride_dfd, cd.id_stride_dfd, cl.id_stride_dfd FROM components_links AS cl " \
                          "JOIN components AS cs ON cl.id_component_src = cs.id " \
                          "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                          "JOIN components_links_var AS clv ON clv.id_link = cl.id " \
                          "WHERE cl.id_component_src = ? AND cd.id_thing = ?"

        sql_left = "SELECT DISTINCT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name, cs.id_thing, cd.id_thing, cl.is_bound_trust, " \
                   "cs.id_stride_dfd, cd.id_stride_dfd, cl.id_stride_dfd FROM components_links AS cl " \
                   "JOIN components AS cs ON cl.id_component_src = cs.id " \
                   "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                   "JOIN components_links_var AS clv ON clv.id_link = cl.id " \
                   "WHERE cl.id_component_src = ? AND clv.id_act > 0 AND cd.id_thing <> ?"

        sql_left_hlc = "SELECT DISTINCT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name, cs.id_thing, cd.id_thing, cl.is_bound_trust, " \
                       "cs.id_stride_dfd, cd.id_stride_dfd, cl.id_stride_dfd FROM components_links AS cl " \
                       "JOIN components AS cs ON cl.id_component_src = cs.id " \
                       "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                       "JOIN components_links_var AS clv ON clv.id_link = cl.id " \
                       "WHERE cl.id_component_src = ? AND clv.id_act > 0 AND cd.id_thing == ?"
        # get CP and Sensor
        # cur.execute(sql_normal, (Constant.DB_ID_CP, Constant.DB_ID_SENSOR, id_project, id_project,))
        # rows_link_a = cur.fetchall()
        # result_list = construct_stride_object(cur, rows_link_a, False, False)

        cur.execute("SELECT id FROM components WHERE id_thing = ? AND id_project = ? AND is_external_component = 0 AND is_human = 0", (Constant.DB_ID_CONTROLLER, id_project,))
        rows = cur.fetchall()

        for row in rows:
            id_controller = row[0]

            # get normal connection to controller
            cur.execute(sql_right, (id_controller, Constant.DB_ID_CONTROLLER,))
            rows_link_a = cur.fetchall()
            result_list.extend(construct_stride_feed_object(cur, rows_link_a, False))

            # get normal connection to hlc
            cur.execute(sql_to_hlc, (id_controller, Constant.DB_ID_CONTROLLER,))
            rows_link_b = cur.fetchall()
            result_list.extend(construct_stride_feed_object(cur, rows_link_b, True))

            # get feedback controller to EXT
            cur.execute(sql_to_ext_feed, (id_controller, Constant.DB_ID_EXT_INFORMATION,))
            rows_link_c = cur.fetchall()
            result_list.extend(construct_stride_feed_object(cur, rows_link_c, False))

            # get normal connection to controller
            cur.execute(sql_left, (id_controller, Constant.DB_ID_CONTROLLER,))
            rows_link_d = cur.fetchall()
            result_list.extend(construct_stride_act_object(cur, rows_link_d, False))

            # get normal connection to hlc
            cur.execute(sql_left_hlc, (id_controller, Constant.DB_ID_CONTROLLER,))
            rows_link_e = cur.fetchall()
            result_list.extend(construct_stride_act_object(cur, rows_link_e, True))

    return result_list

# I don't know if it works properly
def select_dfd_links_second(id_project):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        sql_right = "SELECT DISTINCT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name, cs.id_thing, cd.id_thing, cl.is_bound_trust, " \
                    "cs.id_stride_dfd, cd.id_stride_dfd FROM components_links AS cl " \
                    "JOIN components AS cs ON cl.id_component_src = cs.id " \
                    "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                    "WHERE cs.is_human = 0 AND cd.is_human = 0 AND cs.id_thing <> 3 AND cd.id_thing <> 3 AND cs.id_project = ? AND cd.id_project = ?"

        # get normal connection to controller
        cur.execute(sql_right, (id_project, id_project,))
        rows_link_a = cur.fetchall()
        result_list.extend(construct_stride_feed_object(cur, rows_link_a, False))
        result_list.extend(construct_stride_act_object(cur, rows_link_a, False))


    return result_list

def construct_stride_feed_object(cur, row_link, is_hlc):
    result_list = []

    sql_var = "SELECT v.name from variables AS v " \
              "JOIN components_links_var AS clv ON clv.id_var = v.id " \
              "WHERE clv.id_link = ?"

    for row_l in row_link:
        list_var = []
        cur.execute(sql_var, (row_l[0],))
        row_var = cur.fetchall()
        for var in row_var:
            list_var.append(var[0])

        if len(list_var) > 0:
            is_ext = False
            if row_l[5] == Constant.DB_ID_EXT_INFORMATION or row_l[6] == Constant.DB_ID_EXT_INFORMATION:
                is_ext = True
            result_list.append(Component_Link_Stride(row_l[0], row_l[1], row_l[2], row_l[3], row_l[4], row_l[5], row_l[6], [], list_var, is_ext, is_hlc, row_l[7], row_l[8], row_l[9], row_l[10]))

    return result_list

def construct_stride_act_object(cur, row_link, is_hlc):
    result_list = []

    sql_act = "SELECT a.name FROM actions_component AS a " \
             "JOIN components_links_var AS clv ON clv.id_act = a.id " \
             "WHERE clv.id_link = ?"

    for row_l in row_link:
        list_act = []
        cur.execute(sql_act, (row_l[0],))
        row_act = cur.fetchall()
        for act in row_act:
            list_act.append(act[0])

        if len(list_act) > 0:
            is_ext = False
            if row_l[5] == Constant.DB_ID_EXT_INFORMATION or row_l[6] == Constant.DB_ID_EXT_INFORMATION:
                is_ext = True

            result_list.append(Component_Link_Stride(row_l[0], row_l[1], row_l[2], row_l[3], row_l[4], row_l[5], row_l[6], list_act, [], is_ext,is_hlc, row_l[7], row_l[8], row_l[9], row_l[10]))

    return result_list

def select_omitted_links(id_project):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        sql_default = "SELECT DISTINCT cs.name, cd.name, cs.id_thing, cd.id_thing FROM components_links AS cl " \
                      "LEFT JOIN components_links_var AS clv ON clv.id_link = cl.id " \
                      "JOIN components AS cs ON cl.id_component_src = cs.id " \
                      "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                      "WHERE clv.id_link IS NULL AND cs.id_project == ? AND cd.id_project == ?"

        # get normal connection to controller
        cur.execute(sql_default, (id_project, id_project))
        rows = cur.fetchall()
        for row in rows:
            if (row[2] == Constant.DB_ID_ACTUATOR and row[3] == Constant.DB_ID_CP) or (row[2] == Constant.DB_ID_CP and row[3] == Constant.DB_ID_SENSOR):
                result_list.append(row[0] + " -> " + row[1])
    return result_list

def select_empty_links(id_project):
    result = ""

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        sql_default = "SELECT DISTINCT cs.name, cd.name, cs.id_thing, cd.id_thing FROM components_links AS cl " \
                      "LEFT JOIN components_links_var AS clv ON clv.id_link = cl.id " \
                      "JOIN components AS cs ON cl.id_component_src = cs.id " \
                      "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                      "WHERE clv.id_link IS NULL AND cs.id_project == ? AND cd.id_project == ?"

        # get normal connection to controller
        cur.execute(sql_default, (id_project, id_project))
        rows = cur.fetchall()
        for row in rows:
            if (row[2] != Constant.DB_ID_ACTUATOR and row[3] != Constant.DB_ID_CP) and (row[2] != Constant.DB_ID_CP and row[3] != Constant.DB_ID_SENSOR):
                if result == "":
                    result += "Link without control action or feedback\n"
                result += "\t" + row[0] + " -> " + row[1] + "\n"


    return result
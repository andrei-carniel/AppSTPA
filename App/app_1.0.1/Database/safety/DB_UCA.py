import sqlite3
from sqlite3 import Error
import Constant
from Objects.Saf_UCA import Saf_UCA, Saf_UCA_Hazard, Saf_UCA_Context, Saf_UCA_Type, Saf_UCA_Type_Comp


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

def create_table_saf_uca_type():
    sql_query = "CREATE TABLE IF NOT EXISTS saf_uca_type(id INTEGER PRIMARY KEY, description INTEGER NOT NULL );"

    return sql_query

# create all tables if not exists
def create_table_UCA():
    sql_create_goals_table = "CREATE TABLE saf_uca (id INTEGER PRIMARY KEY, id_controller INTEGER NOT NULL, id_uca_type INTEGER NOT NULL, " \
                             "id_control_action INTEGER NOT NULL, order_analysis INTEGER NOT NULL DEFAULT 0, uca_origin TEXT NOT NULL DEFAULT '', " \
                             "is_hazardous INTEGER NOT NULL DEFAULT 0, " \
                             "description	TEXT, " \
                             "FOREIGN KEY(id_controller) REFERENCES components(id) " \
                             "FOREIGN KEY(id_uca_type) REFERENCES saf_uca_type(id) " \
                             "FOREIGN KEY(id_control_action) REFERENCES actions_component(id) )"



    return sql_create_goals_table

def create_table_saf_uca_hazards():
    sql_query = "CREATE TABLE IF NOT EXISTS saf_uca_hazard (id INTEGER PRIMARY KEY, id_uca INTEGER NOT NULL, id_hazard INTEGER NOT NULL, " \
                "FOREIGN KEY(id_uca) REFERENCES saf_uca(id) " \
                "FOREIGN KEY(id_hazard) REFERENCES hazards(id) );"

    return sql_query

def create_table_saf_uca_context():
    sql_query = "CREATE TABLE IF NOT EXISTS saf_uca_context ( id INTEGER PRIMARY KEY, id_uca INTEGER NOT NULL, id_variable INTEGER NOT NULL, id_value INTEGER NOT NULL," \
                "FOREIGN KEY(id_uca) REFERENCES saf_uca(id) " \
                "FOREIGN KEY(id_variable) REFERENCES variables(id) " \
                "FOREIGN KEY(id_value) REFERENCES variables_values(id) );"

    return sql_query

# insert many registers
def insert_to_db(conn, sql, task):
    # create a database connection
    with conn:
        cur = conn.cursor()
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid

# Insert all the saf_uca_time of ontology
def insert_saf_uca_time():
    sql = "INSERT OR REPLACE INTO saf_uca_type(id, description) VALUES (?, ?)"

    conn = create_connection()

    rsql1 = insert_to_db(conn, sql, (Constant.DB_ID_UT_PWO, 'provided in wrong order'))
    rsql2 = insert_to_db(conn, sql, (Constant.DB_ID_UT_PTE, 'provided too early'))
    rsql3 = insert_to_db(conn, sql, (Constant.DB_ID_UT_PTL, 'provided too late'))
    rsql4 = insert_to_db(conn, sql, (Constant.DB_ID_UT_NP, 'not provided'))
    rsql5 = insert_to_db(conn, sql, (Constant.DB_ID_UT_P, 'provided'))
    rsql6 = insert_to_db(conn, sql, (Constant.DB_ID_UT_ATL, 'applied too long'))
    rsql7 = insert_to_db(conn, sql, (Constant.DB_ID_UT_STS, 'stopped too soon'))

def update(id_uca, description_uca):
    conn = create_connection()
    with conn:
        sql = "UPDATE saf_uca SET description = ? WHERE id = ?"
        cur = conn.cursor()
        task = (description_uca, id_uca)
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid

# select all saf_uca_time ordering by name
def select_all_saf_uca_type():
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM saf_uca_type ORDER BY id")

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Saf_UCA_Type(row[0], row[1]))

    return result_list

# select all saf_uca_time ordering by name
def select_all_saf_uca_type_COMP():
    result_uca = []
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM saf_uca_type ORDER BY id")

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Saf_UCA_Type(row[0], row[1]))

        result_uca.append(Saf_UCA_Type_Comp("UCA Type", result_list))

    return result_uca

# select all saf_uca by controller
def select_all_saf_uca_by_controller(id_controller):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT sf.id, sf.id_controller, c.name, sf.id_uca_type, sut.description, sf.id_control_action, ac.name FROM saf_uca AS sf "
                    "JOIN components AS c ON c.id = sf.id_controller "
                    "JOIN saf_uca_type AS sut ON sut.id = sf.id_uca_type "
                    "JOIN actions_component AS ac ON ac.id = sf.id_control_action "
                    "WHERE sf.id_controller = ?", (id_controller,))

        rows = cur.fetchall()

        for row in rows:
            obj = Saf_UCA(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            obj.context_list = select_all_saf_uca_context_by_uca(obj.id)
            obj.hazard_list = select_all_saf_uca_hazard_by_uca(obj.id)

            result_list.append(obj)

    return result_list

# select all saf_uca by control action
def select_all_saf_uca_by_control_action_filtering(id_control_action, uca_origin, is_hazardous):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        sql = "SELECT sf.id, sf.id_controller, c.name, sf.id_uca_type, sut.description, sf.id_control_action, ac.name, sf.uca_origin, sf.is_hazardous, sf.description FROM saf_uca AS sf " \
              "JOIN components AS c ON c.id = sf.id_controller " \
              "JOIN saf_uca_type AS sut ON sut.id = sf.id_uca_type " \
              "JOIN actions_component AS ac ON ac.id = sf.id_control_action " \
              "WHERE sf.id_control_action= ?"

        if uca_origin != "":
            sql += " AND sf.uca_origin = ? AND sf.is_hazardous = ?"

            if is_hazardous:
                tasks = (id_control_action, uca_origin, 1)
            else:
                tasks = (id_control_action, uca_origin, 0)
        else:
            sql += " AND sf.is_hazardous = ?"

            if is_hazardous:
                tasks = (id_control_action, 1)
            else:
                tasks = (id_control_action, 0)

        cur.execute(sql, tasks)

        rows = cur.fetchall()

        for row in rows:
            obj = Saf_UCA(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            obj.context_list = select_all_saf_uca_context_by_uca(obj.id)
            obj.hazard_list = select_all_saf_uca_hazard_by_uca(obj.id)
            obj.uca_origin = row[7]
            obj.description = row[9]

            if row[8] == 1:
                obj.is_hazardous = True
            else:
                obj.is_hazardous = False

            result_list.append(obj)

    return result_list

# select all saf_uca by control action
def select_all_saf_uca_by_controller_filtering(id_controller, uca_origin, is_hazardous):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        sql = "SELECT sf.id, sf.id_controller, c.name, sf.id_uca_type, sut.description, sf.id_control_action, ac.name, sf.uca_origin, sf.is_hazardous, sf.description FROM saf_uca AS sf " \
              "JOIN components AS c ON c.id = sf.id_controller " \
              "JOIN saf_uca_type AS sut ON sut.id = sf.id_uca_type " \
              "JOIN actions_component AS ac ON ac.id = sf.id_control_action " \
              "WHERE sf.id_controller= ?"

        if uca_origin != "":
            sql += " AND sf.uca_origin = ? AND sf.is_hazardous = ?"

            if is_hazardous:
                tasks = (id_controller, uca_origin, 1)
            else:
                tasks = (id_controller, uca_origin, 0)
        else:
            sql += " AND sf.is_hazardous = ?"

            if is_hazardous:
                tasks = (id_controller, 1)
            else:
                tasks = (id_controller, 0)

        cur.execute(sql, tasks)

        rows = cur.fetchall()

        for row in rows:
            obj = Saf_UCA(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            obj.context_list = select_all_saf_uca_context_by_uca(obj.id)
            obj.hazard_list = select_all_saf_uca_hazard_by_uca(obj.id)
            obj.uca_origin = row[7]
            obj.description = row[9]

            if row[8] == 1:
                obj.is_hazardous = True
            else:
                obj.is_hazardous = False

            result_list.append(obj)

    return result_list

# select all saf_uca_context by uca
def select_all_saf_uca_context_by_uca(id_uca):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        # cur.execute("SELECT suc.id, suc.id_uca, suc.id_variable, v.name, suc.id_value, vv.value FROM saf_uca_context AS suc "
        #             "JOIN variables AS v ON v.id = suc.id_variable "
        #             "JOIN variables_values AS vv ON vv.id = suc.id_value "
        #             "WHERE suc.id_uca = ?", (id_uca,))

        cur.execute("SELECT suc.id, suc.id_uca, suc.id_variable, suc.id_value FROM saf_uca_context AS suc WHERE suc.id_uca = ?", (id_uca,))
        rows = cur.fetchall()

        for row in rows:
            var_name = Constant.VAR_ERR
            val_value = Constant.VAL_ERR

            cur.execute("SELECT name FROM variables WHERE id = ?", (row[2],))
            row_var = cur.fetchone()

            if row_var != None:
                var_name = row_var[0]

            cur.execute("SELECT value FROM variables_values WHERE id = ?", (row[3],))
            row_val = cur.fetchone()

            if row_val != None:
                val_value = row_val[0]

            result_list.append(Saf_UCA_Context(row[0], row[1], row[2], var_name, row[3], val_value))
    return result_list

# select all saf_uca_hazard by uca
def select_all_saf_uca_hazard_by_uca(id_uca):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT suh.id, suh.id_uca, suh.id_hazard, h.description, h.id_hazard FROM saf_uca_hazard AS suh "
                    "JOIN hazards AS h ON h.id = suh.id_hazard "
                    "WHERE suh.id_uca = ?", (id_uca,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Saf_UCA_Hazard(row[0], row[1], row[2], row[3], row[4]))

    return result_list

# select all id saf_uca by control action
def select_id_uca_by_control_action(id_control_action):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM saf_uca WHERE id_control_action = ?", (id_control_action,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(row[0])

    return result_list

# insert one register to Table
def insert(id_controller, id_uca_type, ic_control_action, context_list, hazard_list, uca_origin, is_hazardous):
    # create a database connection
    conn = create_connection()
    with conn:
        sql1 = "INSERT INTO saf_uca (id_controller, id_uca_type, id_control_action, uca_origin, is_hazardous) VALUES(?, ?, ?, ?, ?)"
        cur = conn.cursor()
        cur.execute(sql1, (id_controller, id_uca_type, ic_control_action, uca_origin, is_hazardous,))
        id_uca = cur.lastrowid


        sql2 = "INSERT INTO saf_uca_context (id_uca, id_variable, id_value) VALUES (?, ?, ?)"
        for ctx in context_list:
            for vl in ctx.values_list:
                cur.execute(sql2, (id_uca, ctx.variable.id, vl.id,))

        sql3 = "INSERT INTO saf_uca_hazard (id_uca, id_hazard) VALUES (?, ?)"
        for haz in hazard_list:
            cur.execute(sql3, (id_uca, haz.id,))

        conn.commit()
        return id_uca
    return 0

def insert_from_cell(id_controller, id_uca_type, ic_control_action, context_list, hazard_list, uca_origin, is_hazardous):
    # create a database connection
    conn = create_connection()
    with conn:
        sql1 = "INSERT INTO saf_uca (id_controller, id_uca_type, id_control_action, uca_origin, is_hazardous) VALUES(?, ?, ?, ?, ?)"
        cur = conn.cursor()
        cur.execute(sql1, (id_controller, id_uca_type, ic_control_action, uca_origin, is_hazardous,))
        id_uca = cur.lastrowid


        sql2 = "INSERT INTO saf_uca_context (id_uca, id_variable, id_value) VALUES (?, ?, ?)"
        for ctx in context_list:
            cur.execute(sql2, (id_uca, ctx.var_id, ctx.val_id,))

        sql3 = "INSERT INTO saf_uca_hazard (id_uca, id_hazard) VALUES (?, ?)"
        for haz in hazard_list:
            cur.execute(sql3, (id_uca, haz.id,))

        conn.commit()
        return id_uca
    return 0

# select all
def select_all(id_project):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT sf.id, sf.id_controller, c.name, sf.id_uca_type, sut.description, sf.id_control_action, ac.name, sf.is_hazardous, sf.description FROM saf_uca AS sf "
            "JOIN components AS c ON c.id = sf.id_controller "
            "JOIN saf_uca_type AS sut ON sut.id = sf.id_uca_type "
            "JOIN actions_component AS ac ON ac.id = sf.id_control_action "
            "WHERE c.id_project = ? AND sf.is_hazardous = 1 AND c.is_external_component = 0 ORDER BY c.name", (id_project,))
            # "WHERE c.id_project = ? AND sf.is_hazardous = 1 AND c.is_external_component = 0 sf.uca_origin = ? ORDER BY c.name", (id_project, uca_origin,))

        rows = cur.fetchall()

        for row in rows:
            obj = Saf_UCA(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            obj.context_list = select_all_saf_uca_context_by_uca(obj.id)
            obj.hazard_list = select_all_saf_uca_hazard_by_uca(obj.id)
            obj.description = row[8]

            result_list.append(obj)

    return result_list

def delete(id_uca):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM saf_loss_scenario_req where id_uca = ?", (id_uca,))
        cur.execute("DELETE FROM saf_uca_hazard WHERE id_uca = ?", (id_uca,))
        cur.execute("DELETE FROM saf_uca_context WHERE id_uca = ?", (id_uca,))
        cur.execute("DELETE FROM saf_uca WHERE id = ?", (id_uca,))
        cur.execute("DELETE FROM saf_loss_scenario_req WHERE id_uca = ?", (id_uca,))
        conn.commit()
        return cur.lastrowid

def delete_by_control_action(id_control_action):
    # create a database connection
    conn = create_connection()
    list_id_uca = select_id_uca_by_control_action(id_control_action)
    with conn:
        cur = conn.cursor()

        for id_uca in list_id_uca:
            cur.execute("DELETE FROM saf_loss_scenario_req where id_uca = ?", (id_uca,))
            cur.execute("DELETE FROM saf_uca_hazard WHERE id_uca = ?", (id_uca,))
            cur.execute("DELETE FROM saf_uca_context WHERE id_uca = ?", (id_uca,))
            cur.execute("DELETE FROM saf_uca WHERE id = ?", (id_uca,))
            cur.execute("DELETE FROM saf_loss_scenario_req WHERE id_uca = ?", (id_uca,))
        conn.commit()
        return

def select_string_uca_by_id(id_uca):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT sf.id, sf.id_controller, c.name, sf.id_uca_type, sut.description, sf.id_control_action, ac.name, sf.is_hazardous, sf.description FROM saf_uca AS sf "
            "JOIN components AS c ON c.id = sf.id_controller "
            "JOIN saf_uca_type AS sut ON sut.id = sf.id_uca_type "
            "JOIN actions_component AS ac ON ac.id = sf.id_control_action "
            "WHERE sf.id = ?", (id_uca,))

        row = cur.fetchone()

        if row == None:
            return ""
        else:

            # obj = Saf_UCA(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            # obj.context_list = select_all_saf_uca_context_by_uca(obj.id)
            # obj.hazard_list = select_all_saf_uca_hazard_by_uca(obj.id)
            # obj.description = row[8]

            #(id, id_controller, name_controller, id_uca_type, description_uca_type, id_action, name_action, context_list=[], hazard_list=[], uca_origin="", is_hazardous=0, description="")

            text_context = ""
            for context in select_all_saf_uca_context_by_uca(row[0]):
                if text_context != "":
                    text_context += ", "
                text_context += context.variable_name + " is " + context.variable_value

            item_uca_u = row[2] + " " + row[4] + " " + row[6]
            if text_context == "":
                item_uca_u += " in any context."
            else:
                item_uca_u += " when " + text_context + ". "

            return item_uca_u

    return result_list

import sqlite3
from sqlite3 import Error

import Constant

from Database.safety import DB_Loss_Scenario_Req, DB_Hazards, DB_Components_Links, DB_Actions, DB_Components, DB_Losses, \
    DB_Safety_Constraints, DB_Projects, DB_Goals, DB_Actions_Components, DB_Assumptions, DB_UCA, DB_Project_Files, \
    DB_Saf_Priority
from Objects.Thing import Thing



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


# create one table
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Error as e:
        print(e)

# create one table
def alter_table(conn, alter_table_sql):
    try:
        c = conn.cursor()
        c.execute(alter_table_sql)
        conn.commit()
    except Error as e:
        print(e)

# create all tables if not exists
def create_all_tables():

    # create a database connection
    conn = create_connection()

    # create tables
    if conn is not None:
        create_table(conn, DB_Projects.create_table())
        create_table(conn, DB_Assumptions.create_table())
        create_table(conn, DB_Goals.create_table())
        create_table(conn, DB_Losses.create_table())
        create_table(conn, DB_Hazards.create_table_hazards())
        create_table(conn, DB_Hazards.create_table_hazards_losses())
        create_table(conn, DB_Safety_Constraints.create_all_tables_safety_constraints())
        create_table(conn, DB_Safety_Constraints.create_all_tables_safety_constraints_hazards())
        create_table(conn, table_things())
        insert_things(conn)

        create_table(conn, DB_Components.create_table())
        create_table(conn, create_table_variables())
        create_table(conn, create_table_variables_values())
        create_table(conn, DB_Actions.create_table())
        insert_actions(conn)

        create_table(conn, DB_Actions_Components.create_table())
        create_table(conn, DB_Components_Links.create_table())
        create_table(conn, DB_Components_Links.create_table_component_link_var())
        create_table(conn, DB_UCA.create_table_saf_uca_type())
        create_table(conn, DB_UCA.create_table_UCA())
        create_table(conn, DB_UCA.create_table_saf_uca_hazards())
        create_table(conn, DB_UCA.create_table_saf_uca_context())
        DB_UCA.insert_saf_uca_time()

        create_table(conn, DB_Loss_Scenario_Req.create_table())
        alter_table(conn, "ALTER TABLE saf_uca ADD description TEXT ''")


        alter_table(conn, "ALTER TABLE components ADD COLUMN is_human INTEGER NOT NULL DEFAULT 0")
        alter_table(conn, "ALTER TABLE components_links ADD COLUMN is_bound_trust INTEGER NOT NULL DEFAULT 0")
        alter_table(conn, "ALTER TABLE components ADD COLUMN id_stride_dfd INTEGER REFERENCES sec_stride_dfd(id);")
        alter_table(conn, "ALTER TABLE components_links ADD COLUMN id_stride_dfd INTEGER NOT NULL DEFAULT 2;")

        create_table(conn, DB_Project_Files.create_table())
        alter_table(conn, "ALTER TABLE  ADD COLUMN priority INTEGER NOT NULL DEFAULT 0")

        create_table(conn, DB_Saf_Priority.create_table())
        alter_table(conn, "ALTER TABLE saf_loss_scenario_req ADD COLUMN id_priority INTEGER DEFAULT 1 REFERENCES saf_priority(id);")

        alter_table(conn, "ALTER TABLE saf_loss_scenario_req ADD COLUMN mechanism TEXT DEFAULT '';")

        alter_table(conn, "ALTER TABLE saf_loss_scenario_req ADD COLUMN performance_req TEXT DEFAULT ''")

    else:
        print("Error! cannot create the database connection.")

# return the sql query for things
def table_things():
    sql_query = "CREATE TABLE IF NOT EXISTS things (id INTEGER PRIMARY KEY, " \
                "name TEXT NOT NULL, " \
                "ontology_name TEXT NOT NULL);"

    return sql_query

# Insert all the things of ontology
def insert_things(conn):
    sql = "INSERT OR REPLACE INTO things(id, name, ontology_name) VALUES(?, ?, ?)"

    rsql1 = insert_to_db(conn, sql, (Constant.DB_ID_CONTROLLER, 'Controller', Constant.CONTROLLER))
    rsql2 = insert_to_db(conn, sql, (Constant.DB_ID_ACTUATOR, 'Actuator', Constant.ACTUATOR))
    rsql3 = insert_to_db(conn, sql, (Constant.DB_ID_CP, 'Controlled Process', Constant.CONTROLLED_PROCESS))
    rsql4 = insert_to_db(conn, sql, (Constant.DB_ID_SENSOR, 'Sensor', Constant.SENSOR))
    rsql5 = insert_to_db(conn, sql, (Constant.DB_ID_INPUT, 'Input', Constant.INPUT))
    rsql6 = insert_to_db(conn, sql, (Constant.DB_ID_OUTPUT, 'Output', Constant.OUTPUT))
    rsql7 = insert_to_db(conn, sql, (Constant.DB_ID_EXT_INFORMATION, 'External Information', Constant.EXTERNAL_INFORMATION))
    rsql8 = insert_to_db(conn, sql, (Constant.DB_ID_ALGORITHM, 'Algorithm', Constant.ALGORITHM))
    rsql9 = insert_to_db(conn, sql, (Constant.DB_ID_PROCESS_MODEL, 'Process Model', Constant.PROCESS_MODEL))
    rsql10 = insert_to_db(conn, sql, (Constant.DB_ID_ENV_DISTURBANCES, 'Environmental Disturbances', Constant.ENVIRONMENTAL_DISTURBANCES))
    rsql11 = insert_to_db(conn, sql, (Constant.DB_ID_HLC, 'High_level Controller', Constant.HIGH_LEVEL_CONTROLLER))

# Insert all actions of ontology
def insert_actions(conn):
    sql = "INSERT OR REPLACE INTO actions(id, source, destiny, name, name_ontology, name_link) VALUES(?, ?, ?, ?, ?, ?)"

    rsql1 = insert_to_db(conn, sql, (Constant.DB_ID_ACT_CACA, Constant.DB_ID_CONTROLLER, Constant.DB_ID_ACTUATOR, 'Control Action from Controller to Actuator', 'Control_action_actuator', ''))
    rsql2 = insert_to_db(conn, sql, (Constant.DB_ID_ACT_CACA, Constant.DB_ID_CONTROLLER, Constant.DB_ID_CP, 'Control Action from Controller to Controlled Process (CP)', 'Control_action_CP', ''))
    rsql3 = insert_to_db(conn, sql, (Constant.DB_ID_ACT_FCP, Constant.DB_ID_SENSOR, Constant.DB_ID_CONTROLLER, 'Feedback of Controlled Process', 'Feedback_of_CP', ''))
    rsql4 = insert_to_db(conn, sql, (Constant.DB_ID_ACT_CAHC, Constant.DB_ID_HLC, Constant.DB_ID_CONTROLLER, 'Control Action from High-level Controller (HLC) to Controller', 'Control_action_HLC_controller', ''))
    rsql5 = insert_to_db(conn, sql, (Constant.DB_ID_ACT_CAHCP, Constant.DB_ID_HLC, Constant.DB_ID_CP, 'Control Action from High-level Controller (HLC) to Controlled Process (CP)', 'Control_action_HLC_CP', ''))
    rsql6 = insert_to_db(conn, sql, (Constant.DB_ID_ACT_FCH, Constant.DB_ID_CONTROLLER, Constant.DB_ID_HLC, 'Feedback of Controller to High-level Controller (HLC)', 'Feedback_of_controller', ''))

# insert many registers to Table Things
def insert_to_db(conn, sql, task):
    # create a database connection
    try:
        with conn:
            cur = conn.cursor()
            cur.execute(sql, task)
            conn.commit()
            return cur.lastrowid
    except Error as e:
        print(e)

# select all things ordering by name
def select_all_things():
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM things ORDER BY name")

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Thing(row[0], row[1], row[2]))

    return result_list

# select all things ordering by name
def select_thing_by_id(id_thing):

    result = Thing(0, "null", "null")

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM things WHERE id = ? ORDER BY name", (id_thing,))

        rows = cur.fetchall()

        for row in rows:
            result = Thing(row[0], row[1], row[2])

    return result

# select things by name
def select_thing_by_ontology_name(name_thing):
    """
    Query tasks by all rows
    :return: List of Losses
    """
    result = None

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM things WHERE ontology_name = ?", (name_thing,))

        row = cur.fetchone()

        # for row in rows:
        if row != None:
            result = Thing(row[0], row[1], row[2])

    return result

# select things by name
def select_thing_name_by_ontology_name(name_thing):
    """
    Query tasks by all rows
    :return: List of Losses
    """
    result = ""

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT t.name FROM things AS t WHERE t.ontology_name = ?", (name_thing,))

        row = cur.fetchone()

        # for row in rows:
        if row != None:
            result = row[0]

    return result

# return the sql query for variables
def create_table_variables():
    sql_query = "CREATE TABLE IF NOT EXISTS variables (id INTEGER PRIMARY KEY AUTOINCREMENT, id_component INTEGER NOT NULL, id_project INTEGER NOT NULL, " \
                "name TEXT NOT NULL, begin_date TEXT NOT NULL, edited_date TEXT, " \
                "FOREIGN KEY(id_component) REFERENCES components(id) " \
                "FOREIGN KEY(id_project) REFERENCES projects(id) " \
                ");"

    return sql_query

# return the sql query for values
def create_table_variables_values():
    sql_query = "CREATE TABLE IF NOT EXISTS variables_values (id INTEGER PRIMARY KEY AUTOINCREMENT, id_variable INTEGER NOT NULL, value TEXT NOT NULL, " \
                "begin_date TEXT NOT NULL, edited_date TEXT, " \
                "FOREIGN KEY(id_variable) REFERENCES variables(id) );"

    return sql_query
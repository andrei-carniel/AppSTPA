import sqlite3
from sqlite3 import Error

import Constant
from Database import DB
from Database.safety import DB_Components, DB_Variables_Values

# make a connection
from Objects.Var_Values_Aux import Var_Values_Aux, Var_Values_Comp
from Objects.Variables import Variables


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
    sql_query = "CREATE TABLE IF NOT EXISTS variables (id INTEGER PRIMARY KEY AUTOINCREMENT, id_component INTEGER NOT NULL, id_project INTEGER NOT NULL, " \
                "name TEXT NOT NULL, begin_date TEXT NOT NULL, edited_date TEXT, " \
                "FOREIGN KEY(id_component) REFERENCES components(id) " \
                "FOREIGN KEY(id_project) REFERENCES projects(id) );"

    return sql_query

# insert one register to Table
def insert(var):
    conn = create_connection()
    with conn:
        sql = "INSERT INTO variables (id_component, id_project, name, begin_date) VALUES(?, ?, ?, ?)"
        cur = conn.cursor()
        task = (var.id_component, var.id_project,var. name, var.begin_date)
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid

def update(var):
    conn = create_connection()
    with conn:
        sql = "UPDATE variables SET name = ?, edited_date = ? WHERE id = ?"
        cur = conn.cursor()
        task = (var. name, var.edited_date, var.id)
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid

# update one register to Table
def delete(var):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM variables WHERE id = ?", (var.id,))
        conn.commit()
        DB_Variables_Values.delete_by_variable(var.id)
        return cur.lastrowid

# update one register to Table
def delete_by_id (var_id):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM variables WHERE id = ?", (var_id,))
        cur.execute("DELETE FROM components_links_var WHERE id_var = ?", (var_id,))
        conn.commit()
        DB_Variables_Values.delete_by_variable(var_id)
        return cur.lastrowid

def delete_by_component(comp_id):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM variables WHERE id_component = ?", (comp_id,))
        rows = cur.fetchall()

        for row in rows:
            # var_id = row[0]
            delete_by_id(row[0])

        conn.commit()
        return cur.lastrowid

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



# select all losses ordering by id_loss
def select_variables_with_value_by_component_project(id_component, id_project):
    """
    Query tasks by all rows
    :return: List of Losses
    """
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM variables WHERE id_component = ? AND id_project = ?", (id_component, id_project,))

        rows = cur.fetchall()

        for row in rows:
            variable = Variables(row[0], row[1], row[2], row[3], row[4], row[5])
            result_list.append(Var_Values_Aux(variable.name, variable, DB_Variables_Values.select_values_by_variable(variable.id)))


    return result_list

def select_variables_by_component_project(id_component, id_project):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM variables WHERE id_component = ? AND id_project = ?", (id_component, id_project,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Variables(row[0], row[1], row[2], row[3], row[4], row[5]))

    return result_list

# select variables with values
def select_variables_with_value_by_thing_project_analysis(name_individual, id_project):
    """
    Query tasks by all rows
    :return: List of Losses
    """
    result_list = []
    thing = DB.select_thing_by_ontology_name(name_individual)
    if thing != None:
        component_list = DB_Components.select_component_by_thing_project_analysis(thing.id, id_project)

        # create a database connection
        conn = create_connection()
        with conn:
            cur = conn.cursor()
            for component in component_list:
                cur.execute("SELECT * FROM variables WHERE id_component = ? AND id_project = ?", (component.id, id_project,))

                rows = cur.fetchall()

                for row in rows:
                    variable = Variables(row[0], row[1], row[2], row[3], row[4], row[5])
                    result_list.append(Var_Values_Aux(variable.name, DB_Variables_Values.select_values_by_variable(variable.id)))
    else:
        # create a database connection
        conn = create_connection()
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT v.id, v.id_component, v.id_project, v.name, v.begin_date, v.edited_date FROM variables AS v "
                        "JOIN components AS c ON v.id_component = c.id "
                        "JOIN actions AS a ON a.source = c.id_thing "
                        "WHERE c.id_project = ? AND a.name_ontology = ?",
                        (id_project, name_individual))

            rows = cur.fetchall()

            for row in rows:
                variable = Variables(row[0], row[1], row[2], row[3], row[4], row[5])
                result_list.append(Var_Values_Aux(variable.name, DB_Variables_Values.select_values_by_variable(variable.id)))

    return result_list

# select all variables with values
def select_variables_with_value_by_name_project_analysis(name_individual, id_project):
    """
    Query tasks by all rows
    :return: List of Losses
    """
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT v.id, v.id_component, v.id_project, v.name, v.begin_date, v.edited_date FROM variables AS v "
                    "JOIN components AS c ON v.id_component = c.id "
                    "JOIN actions AS a ON a.source = c.id_thing "
                    "WHERE c.id_project = ? AND a.name_ontology = ?",
                    (id_project, name_individual))

        rows = cur.fetchall()

        for row in rows:
            variable = Variables(row[0], row[1], row[2], row[3], row[4], row[5])
            result_list.append(Var_Values_Aux(variable.name, DB_Variables_Values.select_values_by_variable(variable.id)))

    return result_list

def select_variables_with_value_by_controller(id_controller):
    """
    Query tasks by all rows
    :return: List of Losses
    """
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT v.id, v.id_component, v.id_project, v.name, v.begin_date, v.edited_date from variables AS v "
                    "JOIN components AS c ON c.id = v.id_component WHERE c.id = ?", (id_controller,))

        rows = cur.fetchall()

        for row in rows:
            variable = Variables(row[0], row[1], row[2], row[3], row[4], row[5])
            result_list.append(Var_Values_Aux(variable.name, variable, DB_Variables_Values.select_values_by_variable(variable.id)))

    return result_list

def select_variables_with_value_by_controller_project_link(id_controller, id_project, id_link):
    """
    Query tasks by all rows
    :return: List of Losses
    """
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT v.id, v.id_component, v.id_project, v.name, v.begin_date, v.edited_date from variables AS v "
                    "JOIN components_links_var AS clv ON clv.id_var = v.id "
                    "WHERE v.id_component = ? AND v.id_project = ? AND clv.id_link = ?", (id_controller, id_project, id_link,))

        rows = cur.fetchall()

        for row in rows:
            variable = Variables(row[0], row[1], row[2], row[3], row[4], row[5])
            result_list.append(Var_Values_Aux(variable.name, variable, DB_Variables_Values.select_values_by_variable(variable.id)))

    return result_list

def select_variables_names_by_controller_and_component(id_controller, id_component):
    """
    Query tasks by all rows
    :return: List of Losses
    """
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT v.id, v.id_component, v.id_project, v.name, v.begin_date,  v.edited_date, v.id_component_link from variables AS v "
                    "JOIN components_links AS cl ON v.id_component_link  = cl.id "
                    "JOIN components AS c ON c.id = cl.id_component_dst "
                    "WHERE c.id = ? AND v.id_component = ?", (id_controller, id_component, ))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Variables(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    return result_list

def select_variables_with_value_by_variable_ID(id_var):
    result_list = []

    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT v.id, v.id_component, v.id_project, v.name, v.begin_date,  v.edited_date from variables AS v "
                    "WHERE v.id = ?", (id_var,))

        rows = cur.fetchall()

        for row in rows:
            variable = Variables(row[0], row[1], row[2], row[3], row[4], row[5])
            result_list.append(Var_Values_Comp(variable.name, variable, DB_Variables_Values.select_values_by_variable(variable.id)))

    return result_list

def select_variables_with_value_by_project_controller_FOR_UCA(id_project, id_controller):
    result_list = []

    conn = create_connection()
    with conn:
        cur = conn.cursor()

        cur.execute(
            "SELECT v.id, v.id_component, v.id_project, v.name, v.begin_date,  v.edited_date from variables AS v "
            "WHERE v.id_component = ?", (id_controller,))
        rows = cur.fetchall()

        for row in rows:
            variable = Variables(row[0], row[1], row[2], row[3], row[4], row[5])
            result_list.append(
                Var_Values_Comp(variable.name, variable, DB_Variables_Values.select_values_by_variable(variable.id)))


        cur.execute("SELECT v.id, v.id_component, v.id_project, v.name, v.begin_date,  v.edited_date, c.name from variables AS v "
                    "JOIN components AS c ON c.id = v.id_component "
                    "WHERE c.comp_father = ? AND c.id_thing = 7 ", (id_controller,))
        rows = cur.fetchall()

        for row in rows:
            variable = Variables(row[0], row[1], row[2], row[3], row[4], row[5])
            result_list.append(Var_Values_Comp(variable.name, variable, DB_Variables_Values.select_values_by_variable(variable.id)))


        cur.execute("SELECT v.id, v.id_component, v.id_project, v.name, v.begin_date,  v.edited_date, c.name from variables AS v "
                    "JOIN components AS c ON c.id = v.id_component "
                    "WHERE c.id_project = ? AND c.id_thing = 3", (id_project,))
        rows = cur.fetchall()

        for row in rows:
            variable = Variables(row[0], row[1], row[2], row[3], row[4], row[5])
            result_list.append(Var_Values_Comp(variable.name, variable, DB_Variables_Values.select_values_by_variable(variable.id)))

    return result_list

# def select_variables_not_external_by_project(id_project):
#     result_list = []
#
#     # create a database connection
#     conn = create_connection()
#     with conn:
#         cur = conn.cursor()
#         cur.execute("SELECT v.id, v.id_component, v.id_project, v.name, v.begin_date, v.edited_date FROM variables AS v "
#                     "JOIN components AS c ON c.id = v.id_component "
#                     "WHERE v.id_project = ? AND c.is_external_component = 0", (id_project,))
#
#         rows = cur.fetchall()
#
#         for row in rows:
#             result_list.append(Variables(row[0], row[1], row[2], row[3], row[4], row[5]))
#
#     return result_list

def select_name_variables_by_controller(id_controller):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM variables WHERE id_component = ?", (id_controller,))
        rows = cur.fetchall()

        sql = "SELECT cs.name, cd.name FROM components_links AS cl " \
              "JOIN components AS cs ON cl.id_component_src = cs.id " \
              "JOIN components AS cd ON cl.id_component_dst = cd.id " \
              "JOIN components_links_var AS clv ON clv.id_link = cl.id " \
              "WHERE clv.id_var = ?"

        for row in rows:
            links = ""
            cur.execute(sql, (row[0],))
            rows_links = cur.fetchall()

            for row_l in rows_links:
                links += " (" + row_l[0] + " -> " + row_l[1] + ")"

            result_list.append(row[1] + links)

    return result_list

def select_variables_warning(id_project):
    result = ""

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT v.id, v.name FROM variables AS v "
                    "JOIN components AS c ON c.id = v.id_component "
                    "WHERE c.id_thing = 1 AND c.id_project = ?", (id_project,))

        rows = cur.fetchall()

        for row in rows:
            cur.execute("SELECT count(id) FROM variables_values WHERE id_variable = ?", (row[0],))
            row_count = cur.fetchone()

            if row_count != None:
                if row_count[0] < 2:
                    if result == "":
                        result += "Variables with less than 2 values\n"
                    result += "\t" + row[1] + "\n"

    return result
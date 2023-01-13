import sqlite3
from sqlite3 import Error

import Constant


# make a connection
from Database.safety import DB_UCA
from Objects.Loss_Scenario_Req import Loss_Scenario_Req


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
    sql_create_goals_table = "CREATE TABLE IF NOT EXISTS saf_loss_scenario_req (id INTEGER PRIMARY KEY AUTOINCREMENT, id_controller INTEGER NOT NULL, " \
                             "id_uca INTEGER NOT NULL, id_project INTEGER NOT NULL, id_comp_cause INTEGER NOT NULL, id_comp_src INTEGER NOT NULL, " \
                             "id_comp_dst INTEGER NOT NULL, requirement TEXT NOT NULL, cause TEXT NOT NULL, " \
                             "FOREIGN KEY(id_controller) REFERENCES components(id) " \
                             "FOREIGN KEY(id_uca) REFERENCES saf_uca(id) " \
                             "FOREIGN KEY(id_project) REFERENCES projects(id) " \
                             "FOREIGN KEY(id_comp_cause) REFERENCES components(id) " \
                             "FOREIGN KEY(id_comp_src) REFERENCES components(id) " \
                             "FOREIGN KEY(id_comp_dst) REFERENCES components(id) );"

    return sql_create_goals_table


# insert one register to Table Goals
def insert(req):
    # create a database connection
    conn = create_connection()
    with conn:
        sql = "INSERT INTO saf_loss_scenario_req (id_controller, id_uca, id_project, id_comp_cause, id_comp_src, id_comp_dst, requirement, cause, mechanism) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cur = conn.cursor()
        aux_cause = " ".join(req.cause.split())
        aux_recommendation = " ".join(req.requirement.split())
        task = (req.id_controller, req.id_uca, req.id_project, req.id_comp_cause, req.id_comp_src, req.id_comp_dst, aux_recommendation, aux_cause, req.mechanism)
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid

def update(id, cause, recommendation, mechanism, performance_req):
    # create a database connection
    conn = create_connection()
    with conn:
        sql = "UPDATE saf_loss_scenario_req SET cause = ?, requirement = ?, mechanism = ?, performance_req = ? WHERE id = ?"
        cur = conn.cursor()
        aux_cause = " ".join(cause.split())
        aux_recommendation = " ".join(recommendation.split())
        task = (aux_cause, aux_recommendation, mechanism, performance_req, id)
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid

# update one register to Table Goals
def delete_by_id(req_id):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        # cur.execute("DELETE FROM pef_saf_res_requirement WHERE id_saf_requirement = ?", (req_id,))
        cur.execute("DELETE FROM saf_loss_scenario_req WHERE id = ?", (req_id,))
        conn.commit()
        return cur.lastrowid

def select_all_requirements_by_project_uca(id_project, id_uca):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        # cur.execute("SELECT * FROM saf_loss_scenario_req WHERE id_project = ? AND id_uca = ?", (id_project, id_uca,))
        cur.execute("SELECT lsr.id, lsr.id_controller, lsr.id_uca, lsr.id_project, lsr.id_comp_cause, lsr.id_comp_src, lsr.id_comp_dst, lsr.requirement, "
                    "lsr.cause, lsr.mechanism, cs.name, cd.name, cc.name, lsr.performance_req "
                    "FROM saf_loss_scenario_req AS lsr "
                    "JOIN components AS cs ON cs.id = lsr.id_comp_src "
                    "JOIN components AS cd ON cd.id = lsr.id_comp_dst "
                    "JOIN components AS cc ON cc.id = lsr.id_comp_cause "
                    "WHERE lsr.id_project = ? AND lsr.id_uca = ?", (id_project, id_uca,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Loss_Scenario_Req(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13]))

    return result_list

def select_requirements_by_controller_uca(id_controller, id_uca):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()

        sql = "SELECT DISTINCT lsr.id, lsr.id_controller, lsr.id_uca, lsr.id_project, lsr.id_comp_cause, lsr.id_comp_src, lsr.id_comp_dst, lsr.requirement, " \
                    "lsr.cause, lsr.mechanism, cs.name, cd.name, cc.name, lsr.performance_req " \
                    "FROM saf_loss_scenario_req AS lsr " \
                    "JOIN components AS cs ON cs.id = lsr.id_comp_src " \
                    "JOIN components AS cd ON cd.id = lsr.id_comp_dst " \
                    "JOIN components AS cc ON cc.id = lsr.id_comp_cause " \
					"JOIN saf_uca AS sf ON sf.id = lsr.id_uca " \
                    "WHERE lsr.id_controller = ? AND sf.id_uca_type = ?"

        # cur.execute("SELECT id from components WHERE comp_father = ?", (id_controller,))
        # rows_comp = cur.fetchall()
        #
        # for r in rows_comp:
        #     sql += " OR lsr.id_comp_cause = " + str(r[0])
        #
        # sql += " AND sf.id_uca_type = ?"

        cur.execute(sql, (id_controller, id_uca,))
        rows = cur.fetchall()

        for row in rows:
            result_list.append(Loss_Scenario_Req(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13]))

    return result_list

def select_requirements_by_controller_resource(id_controller, id_resource):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()

        sql = "SELECT DISTINCT lsr.id, lsr.id_controller, lsr.id_uca, lsr.id_project, lsr.id_comp_cause, lsr.id_comp_src, lsr.id_comp_dst, lsr.requirement, " \
                    "lsr.cause, lsr.mechanism, cs.name, cd.name, cc.name, lsr.performance_req " \
                    "FROM saf_loss_scenario_req AS lsr " \
                    "JOIN components AS cs ON cs.id = lsr.id_comp_src " \
                    "JOIN components AS cd ON cd.id = lsr.id_comp_dst " \
                    "JOIN components AS cc ON cc.id = lsr.id_comp_cause " \
					"JOIN saf_uca AS sf ON sf.id = lsr.id_uca " \
                    "WHERE lsr.id_controller = ?"

        # cur.execute("SELECT id from components WHERE comp_father = ?", (id_controller,))
        # rows_comp = cur.fetchall()
        #
        # for r in rows_comp:
        #     sql += " OR lsr.id_comp_cause = " + str(r[0])

        cur.execute(sql, (id_controller,))
        rows = cur.fetchall()

        # for row in rows:
        #     cur.execute("SELECT count(id) FROM pef_saf_res_requirement WHERE id_saf_requirement = ? AND id_resource = ?", (row[0], id_resource))
        #     row_count = cur.fetchone()
        #
        #     if row_count != None:
        #         if row_count[0] > 0:
        #             result_list.append(Loss_Scenario_Req(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13],
        #                                                  DB_Saf_Pef_Requirement.select_by_requirement_without_connection(cur, row[0], id_resource)))

    return result_list

def select_id_requirement_by_uca(id_uca):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM saf_loss_scenario_req where id_uca = ?", (id_uca,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(row[0])

    return result_list

def select_all(id_project):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        # cur.execute("SELECT * FROM saf_loss_scenario_req WHERE id_project = ? AND id_uca = ?", (id_project, id_uca,))
        cur.execute("SELECT lsr.id, lsr.id_controller, lsr.id_uca, lsr.id_project, lsr.id_comp_cause, lsr.id_comp_src, lsr.id_comp_dst, lsr.requirement, "
                    "lsr.cause, lsr.mechanism, cs.name, cd.name, cc.name , lsr.performance_req "
                    "FROM saf_loss_scenario_req AS lsr "
                    "JOIN components AS cs ON cs.id = lsr.id_comp_src "
                    "JOIN components AS cd ON cd.id = lsr.id_comp_dst "
                    "JOIN components AS cc ON cc.id = lsr.id_comp_cause "
                    "WHERE lsr.id_project = ? AND cs.is_external_component = 0 AND cd.is_external_component = 0", (id_project,))

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Loss_Scenario_Req(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13]))

    return result_list

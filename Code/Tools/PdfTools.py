from datetime import datetime

import Constant
from Database import DB
from Database.safety import DB_Loss_Scenario_Req, DB_Hazards, DB_Components_Links, DB_Components, DB_Losses, \
    DB_Safety_Constraints, DB_Variables, DB_Projects, DB_Goals, DB_Actions_Components, DB_Assumptions, DB_UCA
# from dist.app.reportlab.platypus import Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph

pdf_report_list = []

def Generate_PDF(id_project):
    global pdf_report_list

    try:
        now = datetime.now()
        current_date = now.strftime(Constant.DATETIME_MASK_FILE)

        path_report = Constant.PATH_REPORT + "STPA_report_" + current_date + ".pdf"

        load_STPA_report(id_project, now.strftime(Constant.DATETIME_MASK))

        SimpleDocTemplate(path_report, pagesize=letter,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18).build(pdf_report_list)

        return "New STPA report created.\n\nYou can se the report at " + path_report + "."
    except Exception as e:
        print(e)
        return "Error" + str(e)

def get_label_14_title(text):
    global pdf_report_list
    ptext = '<font size="14"><br/><br/><strong>' + text + '</strong></font>'
    pdf_report_list.append(Paragraph(ptext))
    pdf_report_list.append(Spacer(1, 12))

def get_label_12_bold_subtitle(text):
    global pdf_report_list
    ptext = '<font size="12"><strong>' + text + '</strong></font>'
    pdf_report_list.append(Paragraph(ptext))
    pdf_report_list.append(Spacer(1, 12))

def get_label_12_text(text):
    global pdf_report_list
    ptext = '<font size="12">  ' + text + '</font>'
    pdf_report_list.append(Paragraph(ptext))
    pdf_report_list.append(Spacer(1, 24))

def get_label_11_text(text):
    global pdf_report_list
    ptext = '<font size="11">&nbsp;&nbsp;&nbsp;' + text + '</font>'
    pdf_report_list.append(Paragraph(ptext))
    pdf_report_list.append(Spacer(1, 12))

def load_STPA_report(id_project, current_date):
    global pdf_report_list

    pdf_report_list = []

    list_goals_fifth = DB_Goals.select_all_goals_by_project(id_project)
    list_assumptions_fifth = DB_Assumptions.select_all_assumptions_by_project(id_project)
    list_losses_fifth = DB_Losses.select_all_losses_by_project(id_project)
    list_hazards_fifth = DB_Hazards.select_all_hazards_by_project(id_project)
    list_constraints_fifth = DB_Safety_Constraints.select_all_safety_constraints_by_project(id_project)

    project = DB_Projects.select_project_by_id(id_project)
    get_label_14_title("STPA analysis of " + project.name)
    get_label_12_text(project.description)
    get_label_12_text("Begin date: " + project.begin_date)
    get_label_12_text("Report created at: " + current_date)
    # get_label_12_text("Last update: " + project.edited_date))

    # step one
    get_label_14_title("<br/><br/>Step One - Purpose of the Analysis")
    get_label_12_bold_subtitle("Goals")
    for pos in range(len(list_goals_fifth)):
        get_label_11_text(
            "G-" + str(list_goals_fifth[pos].id_goal) + ": " + list_goals_fifth[pos].description)

    get_label_12_bold_subtitle("Assumptions")
    for pos in range(len(list_assumptions_fifth)):
        get_label_11_text("A-" + str(list_assumptions_fifth[pos].id_assumption) + ": " + list_assumptions_fifth[pos].description)

    get_label_12_bold_subtitle("Losses")
    for pos in range(len(list_losses_fifth)):
        get_label_11_text("L-" + str(list_losses_fifth[pos].id_loss) + ": " + list_losses_fifth[pos].description)

    get_label_12_bold_subtitle("System-level Hazards")
    for pos in range(len(list_hazards_fifth)):
        text = ""
        for loss in list_hazards_fifth[pos].list_of_loss:
            text += "[L-" + str(loss.id_loss_screen) + "] "

        get_label_11_text(
            "H-" + str(list_hazards_fifth[pos].id_hazard) + ": " + list_hazards_fifth[pos].description + " " + text)

    get_label_12_bold_subtitle("Systel-level Safety Constraints")
    for pos in range(len(list_constraints_fifth)):
        text = ""
        for haz in list_constraints_fifth[pos].list_of_hazards:
            text += "[H-" + str(haz.id_haz_screen) + "] "

        get_label_11_text(
            "SSC-" + str(list_constraints_fifth[pos].id_safety_constraint) + ": " + list_constraints_fifth[pos].description + " " + text)

    # step 2
    get_label_14_title("<br/><br/>Step Two - Control Structure")
    get_component_report(id_project, DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_CONTROLLER, id_project), Constant.DB_ID_CONTROLLER)
    get_component_report(id_project, DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_ACTUATOR, id_project), Constant.DB_ID_ACTUATOR)
    get_component_report(id_project, DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_SENSOR, id_project), Constant.DB_ID_SENSOR)
    get_component_report(id_project, DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_EXT_INFORMATION, id_project), Constant.DB_ID_EXT_INFORMATION)
    get_component_report(id_project, DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_CP, id_project), Constant.DB_ID_CP)

    # step 3
    get_label_14_title("<br/>Step Three - Unsafe Control Actions")
    get_label_12_bold_subtitle("Unsafe Control Actions (UCA) and Safety Constraints (SC)")
    count_usc = 0
    list_aux_uca = DB_UCA.select_all(id_project)
    for uca in list_aux_uca:
        count_usc += 1

        text_context = ""
        for context in uca.context_list:
            if text_context != "":
                text_context += ", "
            text_context += context.variable_name + " is " + context.variable_value

        text_haz = ""
        for haz in uca.hazard_list:
            text_haz += "[H-"
            id_hz = 1

            for pos in range(len(list_hazards_fifth)):
                if list_hazards_fifth[pos].id == haz.id_hazard:
                    break
                id_hz += 1
            text_haz += str(id_hz) + "]"

        item_uca_r = "Recommendation " + str(
            count_usc) + ": (Controller: " + uca.name_controller + " - Control Action: " + uca.name_action + ")"
        get_label_11_text(item_uca_r)

        item_uca_u = "UCA-" + str(count_usc) + ": " + uca.name_controller + " " + uca.description_uca_type + " " + uca.name_action
        if text_context == "":
            item_uca_u += " in any context."
        else:
            item_uca_u += " when " + text_context + ". "
        item_uca_u += " " + text_haz
        get_label_11_text(item_uca_u)

        item_uca_u_desc = "Description: "
        if uca.description != None:
            item_uca_u_desc += uca.description
        get_label_11_text(item_uca_u_desc)

        item_uca_s = "SC-" + str(count_usc) + ": " + uca.name_controller + " must " + get_opposite_uca(
            uca.id_uca_type) + " " + uca.name_action
        if text_context == "":
            item_uca_s += " in any context."
        else:
            item_uca_s += " when " + text_context + ". "

        get_label_11_text(item_uca_s)
        get_label_11_text("")

    # step 4
    get_label_14_title("Step Four - Loss Scenarios and Recommendations")
    count_ls = 0
    for rec in DB_Loss_Scenario_Req.select_all(id_project):
        count_ls += 1
        spacer = " -> "
        if Constant.ALGORITHM in rec.name_src or Constant.PROCESS_MODEL_full_name in rec.name_src:
            spacer = " in "

        get_label_11_text("R-" + str(count_ls) + " (" + rec.name_src + spacer + rec.name_dst + "): UCA-" + str(get_number_uca(rec.id_uca, list_aux_uca)))
        get_label_11_text("Cause: " + rec.cause)
        get_label_11_text("Recommendation: " + rec.requirement)
        get_label_11_text("Mechanism: " + rec.mechanism)
        get_label_11_text("")

    # report
    get_label_14_title("\nLink Report")
    list_omitted_links = DB_Components_Links.select_omitted_links(id_project)
    for omt in list_omitted_links:
        get_label_11_text(omt)

def get_number_uca(id_uca, list_aux_uca):
    count = 1
    for uca in list_aux_uca:
        if uca.id == id_uca:
            return count
        count += 1
    return 0

def get_component_report(id_project, list_of_components, id_comp):
    general_name = "Component "

    if (id_comp == Constant.DB_ID_CONTROLLER):
        general_name = "Controller "
    elif (id_comp == Constant.DB_ID_ACTUATOR):
        general_name = "Actuator "
    elif (id_comp == Constant.DB_ID_SENSOR):
        general_name = "Sensor "
    elif (id_comp == Constant.DB_ID_EXT_INFORMATION):
        general_name = "External System "
    elif (id_comp == Constant.DB_ID_CP):
        general_name = "Controlled Process "

    for comp in list_of_components:
        aux_name = general_name + comp.name

        if comp.is_external_component == 1:
            aux_name += " (external of analysis)"

        get_label_12_bold_subtitle(aux_name)

        get_label_12_text("Outgoing connections")
        for link in DB_Components_Links.select_component_links_by_project_and_component(comp.id, True):
            get_label_11_text("    " + link.name_src + " -> " + link.name_dst)
            if id_comp == Constant.DB_ID_CONTROLLER:
                get_component_report_actions(comp.id, id_project, link.id)
                get_component_report_feedback(comp.id, id_project, link.id)

        get_label_12_text("Incoming connections")
        for link in DB_Components_Links.select_component_links_by_project_and_component(comp.id, False):
            get_label_11_text("    " + link.name_src + " -> " + link.name_dst)
            if id_comp == Constant.DB_ID_CONTROLLER:
                get_component_report_actions(comp.id, id_project, link.id)
                get_component_report_feedback(comp.id, id_project, link.id)

        if (id_comp == Constant.DB_ID_CP):
            get_report_cp(id_project, comp.id)

        get_label_11_text(" ")

def get_component_report_actions(id_comp, id_project, id_link):
    list_a = DB_Actions_Components.select_actions_by_component_project_link(id_comp, id_project, id_link)
    if len(list_a) > 0:
        aux_a = ""
        for act in list_a:
            if aux_a != "":
                aux_a += ", "
            aux_a += act.name
        get_label_11_text("\tControl actions: " + aux_a)

def get_component_report_feedback(id_comp, id_project, id_link):
    list_v = DB_Variables.select_variables_with_value_by_controller_project_link(id_comp, id_project, id_link)
    if len(list_v) > 0:
        get_label_11_text("\tFeedbacks (variables and values):")
        aux_v = ""
        for var in list_v:
            aux_v = var.var_name + " ("
            add_comma = False
            for val in var.values_list:
                if add_comma:
                    aux_v += ", " + val.value
                else:
                    aux_v += val.value
                add_comma = True
            aux_v += ")"
            get_label_11_text("\t    " + aux_v)

def get_report_cp(id_project, id_father):
    text_inp = ""
    for comp_i in DB_Components.select_controlled_process_values(id_project, id_father, Constant.DB_ID_INPUT):
        if text_inp != "":
            text_inp += ", "
        text_inp += comp_i

    if text_inp != "":
        get_label_11_text("Input: " + text_inp)

    text_out = ""
    for comp_i in DB_Components.select_controlled_process_values(id_project, id_father, Constant.DB_ID_OUTPUT):
        if text_out != "":
            text_out += ", "
        text_out += comp_i

    if text_out != "":
        get_label_11_text("Output: " + text_out)

    text_env = ""
    for comp_i in DB_Components.select_controlled_process_values(id_project, id_father, Constant.DB_ID_ENV_DISTURBANCES):
        if text_env != "":
            text_env += ", "
        text_env += comp_i

    if text_env != "":
        get_label_11_text("Environmental Disturbances: " + text_env)

def get_opposite_uca(id):
    result = ""

    if id == Constant.provided_in_wrong_order:
        result = "not provide in wrong order"
    elif id == Constant.provided_too_early:
        result = "not provide too early"
    elif id == Constant.provided_too_late:
        result = "not provide too late"
    elif id == Constant.not_provided:
        result = "provide"
    elif id == Constant.provided:
        result = "not provide"
    elif id == Constant.applied_too_long:
        result = "not provide too long"
    elif id == Constant.stopped_too_son:
        result = "not provide to soon"

    return result

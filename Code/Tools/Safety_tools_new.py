import datetime

import Constant
from Database import DB
from Database.safety import DB_Hazards, DB_Components_Links, DB_Actions, DB_Components, DB_Losses, \
    DB_Safety_Constraints, DB_Variables, DB_Variables_Values, DB_Projects, DB_Goals, DB_Actions_Components, \
    DB_Assumptions, DB_UCA
from Objects.Loss import Loss_Scenery
from Objects.Requirement import Requirement
from Objects.Var_Values_Aux import Var_Name_Val, Var_Context_list
from Tools import General_tools, Dictionary


# present the analysis of safety requirements
def get_context_object(var_list, position, context_list, vector):

    if len(var_list) == position:
        vector.append(Var_Context_list("Line " + str(position), context_list))
    else:
        for val in var_list[position].values_list:
            context_list.append(Var_Name_Val(var_list[position].var_name, val.value, val.id_variable, val.id))
            position_aux = position + 1

            get_context_object(var_list, position_aux, context_list, vector)

# present the analysis of safety requirements
def get_context(var_list, position, context, init_text, analysis_file):

    if len(var_list) == position:
        analysis_file.write(init_text + " " + context + "\n")
    else:
        for val in var_list[position].values_list:
            aux_context = context + var_list[position].var_name + " is " + val.value
            position_aux = position + 1

            if (position_aux + 1) == len(var_list):
                aux_context = aux_context + " and "
            elif (position_aux + 1) < len(var_list):
                aux_context = aux_context + ", "

            get_context(var_list, position_aux, aux_context, init_text, analysis_file)

# present the analysis of safety requirements
def get_context_a(var_list, position, context, result_list, is_new):

    if len(var_list) == position:
        # analysis_file.write(init_text + " " + context + "\n")
        result_list.append(Var_Context_list("Line " + str(position), context))
        context = []
    else:

        # if len(var_list[position].values_list) == 0:
        #     position_aux = position + 1
        #
        #     if len(var_list) != position_aux and len(var_list[position_aux].values_list) == 0:
        #         position_aux += 1
        #
        #     get_context_a(var_list, position_aux, context, result_list, False)
        # else:
        for val in var_list[position].values_list:
            aux_context = []
            if not is_new:
                aux_context.extend(context)
            aux_context.append(Var_Name_Val(var_list[position].var_name, val.value, val.id_variable, val.id))
            position_aux = position + 1

            if len(var_list) != position_aux and len(var_list[position_aux].values_list) == 0:
                position_aux += 1

            get_context_a(var_list, position_aux, aux_context, result_list, False)

def get_safety_analysis(onto, id_project, id_controller):
    date_now = datetime.datetime.now()
    analysis_file = open(Constant.ANALYSIS_PATH + "safety_analysis_NEW" + str(date_now.year) + "-" + str(date_now.month) + "-" + str(date_now.day) + ".txt", "w")
    controller = DB_Components.select_component_by_id(id_controller)

    project = DB_Projects.select_project_by_id(id_project)

    # Project information
    analysis_file.write("Project name: " + project.name + ". \nDescription: " + project.description + ".")


    analysis_file.write("\n\n---------- First Step ----------\n")

    # Goals information
    analysis_file.write("\n\nGoals: \n")
    for goal in DB_Goals.select_all_goals_by_project(id_project):
        analysis_file.write("G-" + str(goal.id_goal) + ": " + goal.description + "\n")

    # Assumptions information
    analysis_file.write("\n\nAssumptions: \n")
    for ass in DB_Assumptions.select_all_assumptions_by_project(id_project):
        analysis_file.write("A-" + str(ass.id_assumption) + ": " + ass.description+ "\n")

    # Losses information
    analysis_file.write("\n\nLosses: \n")
    for loss in DB_Losses.select_all_losses_by_project(id_project):
        analysis_file.write("L-" + str(loss.id_loss) + ": " + loss.description+ "\n")

    # Hazards information
    analysis_file.write("\n\nSystem-level Hazards: \n")
    for haz in DB_Hazards.select_all_hazards_by_project_with_loss(id_project):
        analysis_file.write("H-" + str(haz.id_hazard) + ": " + haz.description + " [L-" + str(haz.identifier_loss) + "]\n")

    # Safety Constraints information
    analysis_file.write("\n\nSystem-level Safety Constraints: \n")
    for sc in DB_Safety_Constraints.select_all_safety_constraints_by_project(id_project):
        analysis_file.write("SSC-" + str(sc.id_safety_constraint) + ": " + sc.description + "\n")


    analysis_file.write("\n\n---------- Second Step ----------\n\n")

    # select things
    # select components
    # select links only of source
    # if controller select Control Actions
    # elseif select variables
    components_list = DB_Components.select_all_components_by_project_analysis(id_project)

    things_list = DB.select_all_things()

    for th in things_list:
        analysis_file.write(th.name + ":\n")
        components_list = DB_Components.select_component_by_thing_project_analysis(th.id, id_project)

        for cp in components_list:
            analysis_file.write("- " + cp.name + "\n")

            if th.id != Constant.DB_ID_OUTPUT:
                find_for_source = True
            else:
                find_for_source = False

            link_list = DB_Components_Links.select_component_links_by_project_and_thing(id_project, th.id, find_for_source)

            for link in link_list:
                analysis_file.write("\t" + link.name_src + " -> " + link.name_dst + "\n")

                actions_list = DB_Actions_Components.select_actions_by_component_and_project(link.id_component_src, id_project)

                if len(actions_list) > 0:
                    analysis_file.write("\t\tControl Actions\n")

                    for act in actions_list:
                        analysis_file.write("\t\t\t" + act.name + "\n")

                if th.id != Constant.DB_ID_OUTPUT:
                    variables_list = DB_Variables.select_variables_with_value_by_component_project(link.id_component_src, id_project)
                else:
                    variables_list = DB_Variables.select_variables_with_value_by_component_project(link.id_component_dst, id_project)

                if len(variables_list) > 0:
                    analysis_file.write("\t\tVariables/Feedback\n")

                    for var in variables_list:
                        analysis_file.write("\t\t\t" + var.var_name + ": (")

                        aux = ""

                        for val in var.values_list:
                            if aux != "":
                                aux += ", "
                            aux += val.value
                        aux += ")\n"

                        analysis_file.write(aux)

            analysis_file.write("\n")

    analysis_file.write("\n\n---------- Third Step ----------\n\n")
    uca_individuals_list = General_tools.find_individuals_of_class(onto, Constant.UCA)

    uca_type_list = []
    hazards_list = []
    actions_aux_list = []
    load_contex = False

    analysis_file.write("\nOntology individuals:")
    control_actions_list = []
    for item_uca in uca_individuals_list.name_list:
        analysis_file.write("\n\t" + item_uca)
        if "Control_action_"  in item_uca:
            actions_aux_list. append(item_uca)
            action = DB_Actions.select_action_by_name(item_uca)
            if action != None:
                control_actions_list.extend(DB_Actions_Components.select_components_by_action(action, id_project))
        elif Constant.HAZARDS == item_uca:
            hazards_list = DB_Hazards.select_all_hazards_by_project_with_loss(id_project)
        elif Constant.CONTEXT == item_uca:
            load_contex = True
        elif Constant.UCA_TYPE == item_uca:
            uca_type_list = DB_UCA.select_all_saf_uca_tye()


    controller = DB_Components.select_component_by_id(id_controller)
    analysis_file.write("\n\nSource: ")
    analysis_file.write("\n\t" + controller.name)

    analysis_file.write("\nType:")
    for type in uca_type_list:
        analysis_file.write("\n\t" + type.description)

    analysis_file.write("\nControl Actions:")
    for act in actions_aux_list:
        analysis_file.write("\n\t" + act)

    analysis_file.write("\nHazards:")
    for haz in hazards_list:
        analysis_file.write("\n\tH-" + str(haz.id_hazard) + ": " + haz.description)

    if load_contex:
        analysis_file.write("\n\nContext table\n\n")

        for component_action in control_actions_list:
            context_list = DB_Variables.select_variables_with_value_by_controller(component_action.component.id)
            for acton_component in component_action.actions_list:
                init_text = component_action.component.name + " - TYPE - " + acton_component.name + " when "
                get_context(context_list, 0, "", init_text, analysis_file)

    analysis_file.write("\n\nUCA list")
    uca_list = DB_UCA.select_all_saf_uca_by_controller(id_controller)

    for uca in uca_list:
        text = "UCA-" + str(uca.order_analysis) + " - " + uca.name_controller + " " + uca.description_uca_type + " " + uca.name_action + " when "

        text_context = ""
        for context in uca.context_list:
            if text_context != "":
                text_context += ", "
            text_context += context.variable_name + " is " + context.variable_value

        text += text_context + ". "
        for haz in uca.hazard_list:
            text += "[H-" + str(haz.id_hazard) + "]"

        analysis_file.write("\n" + text)


    analysis_file.write("\n\n---------- Fourth Step ----------\n\n")

    loss_A_list = General_tools.find_individuals_of_class(onto, Constant.LOSS_SCENARIO_A)
    loss_B_list = General_tools.find_individuals_of_class(onto, Constant.LOSS_SCENARIO_B)

    analysis_file.write("\nLoss A side (right): \n")
    analysis_file.write("Name: " + str(loss_A_list.class_parent.name) + "\n")

    for name_individual in loss_A_list.name_list:
        analysis_file.write("\t" + get_name_thing_action(name_individual) + ":\n")
        print_reason_component(onto, controller, DB_Components.select_component_by_name_thing_project_analysis(name_individual, id_project), analysis_file, id_project, Constant.CAUSAL_FACTOR_A)
        print_reason_action(onto, controller, DB_Actions.select_action_by_name_with_component(name_individual, id_project), analysis_file, id_project, Constant.CAUSAL_FACTOR_A)


    analysis_file.write("\n\nLoss B side (left): \n")
    analysis_file.write("Name: " + str(loss_B_list.class_parent.name) + "\n")

    for name_individual in loss_B_list.name_list:
        analysis_file.write("\t" + get_name_thing_action(name_individual) + ":\n")
        print_reason_component(onto, controller, DB_Components.select_component_by_name_thing_project_analysis(name_individual, id_project), analysis_file, id_project, Constant.CAUSAL_FACTOR_B)
        print_reason_action(onto, controller, DB_Actions.select_action_by_name_with_component(name_individual, id_project), analysis_file, id_project, Constant.CAUSAL_FACTOR_B)


    analysis_file.write("\n\n---------- Fifth Step ----------\n\n")

    for name_individual in loss_A_list.name_list:
        step_fifth(onto, id_controller, id_project, name_individual, analysis_file)

    analysis_file.write("\n")

    for name_individual in loss_B_list.name_list:
        step_fifth(onto, id_controller, id_project, name_individual, analysis_file)

    analysis_file.close()

def get_step_four(onto, id_project, controller):
    loss_A_list = General_tools.find_individuals_of_class(onto, Constant.CAUSAL_FACTOR_A)
    loss_B_list = General_tools.find_individuals_of_class(onto, Constant.CAUSAL_FACTOR_B)
    result_list = []

    for name_individual in loss_A_list.name_list:
        r_list = get_reason_component(onto, controller, name_individual, id_project, Constant.CAUSAL_FACTOR_A, "A")
        if len(r_list) > 0:
            result_list.extend(r_list)

    for name_individual in loss_B_list.name_list:
        r_list = get_reason_component(onto, controller, name_individual, id_project, Constant.CAUSAL_FACTOR_B, "B")
        if len(r_list) > 0:
            result_list.extend(r_list)
    return result_list

def step_fifth(onto, id_controller, id_project, name_individual, analysis_file):
    analysis_file.write("\n" + get_name_thing_action(name_individual) + ":")
    components_list = DB_Components.select_component_by_name_thing_project_analysis(name_individual, id_project)

    for comp in components_list:
        analysis_file.write("\n\tList of " + comp.name + ":")
        analysis_file.write("\n\t\tConnection: ")

        for conection in DB_Components_Links.select_component_links_by_project_and_component(comp.id, True):
            analysis_file.write("\n\t\t\t" + conection.name_src + " -> " + conection.name_dst)

        for conection in DB_Components_Links.select_component_links_by_project_and_component(comp.id, False):
            analysis_file.write("\n\t\t\t" + conection.name_src + " -> " + conection.name_dst)


        actions_list = DB_Actions_Components.select_actions_by_component_and_project(comp.id, id_project)

        if len(actions_list) > 0:
            for act in actions_list:
                analysis_file.write("\t\t\t" + act.name + "\n")


        analysis_file.write("\n\t\tFeedback: ")

        if comp.id != Constant.DB_ID_OUTPUT:
            variables_list = DB_Variables.select_variables_with_value_by_component_project(comp.id, id_project)
        else:
            variables_list = DB_Variables.select_variables_with_value_by_component_project(comp.id, id_project)

        if len(variables_list) > 0:
            for var in variables_list:
                analysis_file.write("\n\t\t\t" + var.var_name + ":")

                for val in var.values_list:
                    analysis_file.write("\n\t\t\t\t" + val.value)

        analysis_file.write("\n\n")


    if "Control_action_" in name_individual:

        analysis_file.write("\n\t\tLink: ")

        link_list = General_tools.list_relations_for_link(onto, name_individual)
        for father in link_list.son_class:
            analysis_file.write("\n\t\t\t" + father.parent_class.name)
            for son in father.son_individual_name:
                analysis_file.write("\n\t\t\t\t" + son)

        analysis_file.write("\n\t\tControl Actions: ")

        if Constant.CONTROL_ACTION_HLC_CP != name_individual and Constant.CONTROL_ACTION_HLC_CONTROLLER != name_individual:
            comp_list = DB_Components_Links.select_component_links_by_project_and_thing_and_controller(id_project, Constant.DB_ID_ACTUATOR, id_controller, True)
            for comp in comp_list:
                actions_list = DB_Actions_Components.select_actions_by_component_and_project(comp.id_component_src, id_project)

                for act in actions_list:
                    analysis_file.write("\n\t\t\t" + act.name)

        analysis_file.write("\n\n")

    elif "Feedback_of" in name_individual:

        analysis_file.write("\n\t\tLink: ")

        link_list = General_tools.list_relations_for_link(onto, name_individual)
        for father in link_list.son_class:
            analysis_file.write("\n\t\t\t" + father.parent_class.name)
            for son in father.son_individual_name:
                analysis_file.write("\n\t\t\t\t" + son)

        analysis_file.write("\n\t\tFeedback: ")
        components_list = DB_Components.select_component_by_name_thing_project_analysis(Constant.SENSOR, id_project)

        for comp in components_list:
            variables_list = DB_Variables.select_variables_with_value_by_component_project(comp.id, id_project)

            if len(variables_list) > 0:
                for var in variables_list:
                    analysis_file.write("\n\t\t\t" + var.var_name + ":")

                    for val in var.values_list:
                        analysis_file.write("\n\t\t\t\t" + val.value)

        analysis_file.write("\n\n")

def print_reason_component(onto, controller, reason_list, analysis_file, id_project, destination):
    # print right explanations to factors - components
    for rc in reason_list:
        object_properties_list = General_tools.get_property_list_ontology(onto, rc.ontology_name, destination)
        for cause in get_causal_factor_list(rc.ontology_name, rc.name, id_project, controller, object_properties_list):
            analysis_file.write("\t\t" + cause + "\n")

def print_reason_action(onto, controller, reason_list, analysis_file, id_project, destination):
    # print right explanations to factors - actions
    for act in reason_list:
        object_properties_list = General_tools.get_property_list_ontology(onto, act.name_ontology, destination)
        for cause in get_causal_factor_list(act.name_ontology, act.name, id_project, controller, object_properties_list):
            analysis_file.write("\t\t" + cause + "\n")

def get_reason_component(onto, controller, name_individual, id_project, destination, side):
    # print right explanations to factors - components
    list_reason = []
    # reason_list = DB_Components.select_component_by_name_thing_project_analysis(name_individual, id_project)
    # for rc in reason_list:
    object_properties_list = General_tools.get_property_list_ontology(onto, name_individual, destination)
    for cause in get_causal_factor_list(name_individual, id_project, controller, object_properties_list, side):
        list_reason.append(cause)

    return list_reason

def get_reason_action(onto, controller, reason_list, id_project, destination, side):
    # print right explanations to factors - actions
    list_reason = []
    for act in reason_list:
        object_properties_list = General_tools.get_property_list_ontology(onto, act.name_ontology, destination)
        for cause in get_causal_factor_list(act.name_ontology, act.name, id_project, controller, object_properties_list, side):
            list_reason.append(cause)

    return list_reason

def get_name_thing_action(name):
    name_aux = DB.select_thing_name_by_ontology_name(name)

    if name_aux != "":
        return name_aux

    name_aux = DB_Actions.select_name_by_name_ontology(name)
    return name_aux

# Creates the main list of causal factor
def get_causal_factor_list(causal_factor_name, id_project, controller, object_property_list, side):
    result = []

    if causal_factor_name == Constant.ACTUATOR:
        comp_list = DB_Components_Links.select_component_links_by_project_and_thing_and_controller(id_project, Constant.DB_ID_ACTUATOR, controller.id, True)
        cp = DB_Components.select_one_component_by_thing_project_analysis(Constant.DB_ID_CP, id_project)

        for comp in comp_list:
            actuator = DB_Components.select_component_by_id(comp.id_component_dst)
            for obj in object_property_list:

                if obj.replace("-", " ") == "delayed":
                    cause = "The issued control action delays to be enforced by the " + actuator.name + "."
                    req = "The " + actuator.name + " must be reliable and have periodic maintenance."
                    result.append(Loss_Scenery(side, causal_factor_name, actuator.name, cause, req, controller.id, actuator.id, controller.id, actuator.id, controller.name, actuator.name))

                if obj.replace("-", " ") == "executed":
                    cause = actuator.name + " performs (" + obj.replace("-", " ") + ") a non-issued control action."
                    req = "The " + actuator.name + " must be reliable and have periodic maintenance."
                    result.append(Loss_Scenery(side, causal_factor_name, actuator.name, cause, req, controller.id, actuator.id, controller.id, actuator.id, controller.name, actuator.name))

                if obj.replace("-", " ") == "not executed" and cp != None:
                    cause = actuator.name + " did not received the control action, from " + controller.name + ", or cannot act (" + obj.replace("-", " ") + ") in " + cp.name + "."
                    req = "The " + actuator.name + " must be reliable and have periodic maintenance."
                    result.append(Loss_Scenery(side, causal_factor_name, actuator.name, cause, req, controller.id, actuator.id, controller.id, actuator.id, controller.name, actuator.name))

                if obj.replace("-", " ") == "failure":
                    cause = "The " + actuator.name + " does not perform its functions."
                    req = "The " + actuator.name + " must have ongoing analysis after system modification."
                    result.append(Loss_Scenery(side, causal_factor_name, actuator.name, cause, req, controller.id, actuator.id, controller.id, actuator.id, controller.name, actuator.name))

        return result

    if causal_factor_name == Constant.ALGORITHM:
        comp_list = DB_Components.select_component_by_project_father_thing(id_project, controller.id, Constant.DB_ID_ALGORITHM)

        for alg in comp_list:
            for obj in object_property_list:
                if obj.replace("-", " ") == "incorrect":
                    cause = "An incorrect " + alg.name + " was designed."
                    req = "The " + alg.name + " must be revised AND tested when updated."
                    result.append(Loss_Scenery(side, causal_factor_name + "/Logic", alg.name, cause, req, controller.id, alg.id, alg.id, controller.id, alg.name, controller.name))


                if obj.replace("-", " ") == "ineffective":
                    cause = alg.name + " ineffective after process changes."
                    req = "The " + alg.name + " must be updated AND revised AND tested."
                    result.append(Loss_Scenery(side, causal_factor_name + "/Logic", alg.name, cause, req, controller.id, alg.id, alg.id, controller.id, alg.name, controller.name))


                if obj.replace("-", " ") == "updated":
                    cause = alg.name + " updated incorrectly."
                    req = "The " + alg.name + " must be revised AND tested when updated."
                    result.append(Loss_Scenery(side, causal_factor_name + "/Logic", alg.name, cause, req, controller.id, alg.id, alg.id, controller.id, alg.name, controller.name))

        return result

    if causal_factor_name == Constant.CONTROL_ACTION_ACTUATOR:
        comp_list = DB_Components_Links.select_component_links_by_project_and_thing_and_controller(id_project, Constant.DB_ID_ACTUATOR, controller.id, True)
        cp = DB_Components.select_one_component_by_thing_project_analysis(Constant.DB_ID_CP, id_project)

        if cp == None:
            return result

        for comp in comp_list:
            actions_list = DB_Actions_Components.select_actions_by_component_and_project_join_link(comp.id_component_src, id_project, comp.id_component_dst)
            actuator = DB_Components.select_component_by_id(comp.id_component_dst)

            for obj in object_property_list:
                if len(actions_list) > 0:
                    text = ""
                    position = len(actions_list)

                    for act in actions_list:
                        position -= 1
                        text += act.name

                        if position >= 2:
                            text += ", "
                        elif position >= 1:
                            text += " or "

                    if obj.replace("-", " ") == "missing" and cp != None:
                        cause = controller.name + " does not provide (" + obj.replace("-", " ") + ") control action: " + text + "; to " + actuator.name + "."
                        req = "The process model in " + controller.name + " must represent the " + cp.name + "."
                        result.append(Loss_Scenery(side, causal_factor_name, actuator.name, cause, req, controller.id, actuator.id, controller.id, actuator.id, controller.name, actuator.name))

                    if obj.replace("-", " ") == "missing":
                        cause = "The control action: " + text + " from " + controller.name + " to " + actuator.name + " is " + obj.replace("-"," ") + "."
                        req = "The communication from " + controller.name + " to " + actuator.name + " must be improved."
                        result.append(Loss_Scenery(side, causal_factor_name, actuator.name, cause, req, controller.id, actuator.id, controller.id, actuator.id, controller.name, actuator.name))

                    if obj.replace("-", " ") == "inappropriate" and cp != None:
                        cause = controller.name + " issued an incorrect (" + obj.replace("-", " ") + ") control action: " + text + "; to " + actuator.name + "."
                        req = "The process model in " + controller.name + " must represent the " + cp.name + "."
                        result.append(Loss_Scenery(side, causal_factor_name, actuator.name, cause, req, controller.id, actuator.id, controller.id, actuator.id, controller.name, actuator.name))


        return result

    if causal_factor_name == Constant.CONTROL_ACTION_CP:
        cp = DB_Components.select_one_component_by_thing_project_analysis(Constant.DB_ID_CP, id_project)
        comp_list = DB_Components_Links.select_component_links_by_project_and_thing_and_controller(id_project, Constant.DB_ID_CP, controller.id, True)

        if cp == None:
            return result

        for comp in comp_list:
            # actions_list = DB_Actions_Components.select_actions_by_component_and_project(comp.id_component_src, id_project)
            actions_list = DB_Actions_Components.select_actions_by_component_and_project_join_link(comp.id_component_src, id_project, comp.id_component_dst)

            for obj in object_property_list:
                if len(actions_list) > 0:
                    text = ""
                    position = len(actions_list)

                    for act in actions_list:
                        position -= 1
                        text += act.name

                        if position >= 2:
                            text += ", "
                        elif position >= 1:
                            text += " or "

                    if obj.replace("-", " ") == "missing" and cp != None:
                        cause = controller.name + " does not provide (" + obj.replace("-", " ") + ") the control action: " + text + "; to " + cp.name + "."
                        req = "The process model in " + controller.name + " must represent the " + cp.name + "."
                        result.append(Loss_Scenery(side, causal_factor_name, cp.name, cause, req, controller.id, cp.id, controller.id, cp.id, controller.name, cp.name))

                    if obj.replace("-", " ") == "inappropriate" and cp != None:
                        cause = controller.name + " issued an incorrect (" + obj.replace("-", " ") + ") control action: " + text + "; to " + cp.name + "."
                        req = "The process model in " + controller.name + " must represent the " + cp.name + "."
                        result.append(Loss_Scenery(side, causal_factor_name, cp.name, cause, req, controller.id, cp.id, controller.id, cp.id, controller.name, cp.name))
        return result

    if causal_factor_name == Constant.CONTROLLER:
        for obj in object_property_list:
            if obj.replace("-", " ") == "failure":
                cause = "The " + controller.name + " controller does not perform its functions to send control actions or receive feedback."
                req = "The " + controller.name + " must have ongoing analysis after system modification."
                result.append(Loss_Scenery(side, causal_factor_name, controller.name, cause, req, controller.id, controller.id, controller.id, controller.id, controller.name, controller.name))

        return result

    # OK
    # if causal_factor_name == Constant.EXTERNAL_INFORMATION:
    # if causal_factor_name == Constant.EXTERNAL_INFORMATION_SENT or causal_factor_name == Constant.EXTERNAL_INFORMATION_RECEIVED:
    if causal_factor_name == Constant.EXTERNAL_INFORMATION_RECEIVED:
        comp_list = DB_Components_Links.select_component_links_by_project_and_thing_and_controller(id_project, Constant.DB_ID_EXT_INFORMATION, controller.id, False)

        for comp in comp_list:
            variables_list = DB_Variables.select_variables_with_value_by_component_project(comp.id_component_src, id_project)

            for obj in object_property_list:
                text = ""

                if len(variables_list) > 0:
                    position = len(variables_list)

                    for var in variables_list:
                        position -= 1
                        text += var.var_name

                        if position >= 2:
                            text += ", "
                        elif position >= 1:
                            text += " or "

                cause = comp.name_src + " is " + obj.replace("-", " ")
                if text != "":
                    cause += " value of: " + text + "."
                else:
                    cause += "."

                if obj.replace("-", " ") == "wrong" or obj.replace("-", " ") == "missing":
                    req = "The communication of the external system to " + controller.name + " must be improved."
                    result.append(Loss_Scenery(side, causal_factor_name, comp.name_src, cause, req, controller.id, comp.id_component_src, comp.id_component_src, controller.id, comp.name_src, controller.name))


        return result

    if causal_factor_name == Constant.ENVIRONMENTAL_DISTURBANCES:
        cp_list = DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_CP, id_project)

        for cp in cp_list:
            env_dist_list = DB_Components.select_component_by_project_father_thing(id_project, cp.id, Constant.DB_ID_ENV_DISTURBANCES)
            for env_dist in env_dist_list:
                for obj in object_property_list:
                    if obj.replace("-", " ") == "unidentified disturbance":
                        cause = cp.name + " affected by natural or man made disasters."
                        req = "The " + cp.name + " must be resistant to disasters."
                        result.append(Loss_Scenery(side, causal_factor_name, cp.name, cause, req, controller.id, env_dist.id, env_dist.id, cp.id, env_dist.name, cp.name))

        return result

    if causal_factor_name == Constant.FEEDBACK_OF_CP:
        comp_list = DB_Components_Links.select_component_links_by_project_and_thing_and_controller(id_project, Constant.DB_ID_SENSOR, controller.id, False)
        cp = DB_Components.select_one_component_by_thing_project_analysis(Constant.DB_ID_CP, id_project)

        if cp == None:
            return result

        comp_list_cp = DB_Components_Links.select_component_links_by_project_and_thing_and_controller(id_project, Constant.DB_ID_CP, controller.id, False)

        # link controlled process -> controller
        for link2 in comp_list_cp:
            variables_list = DB_Variables.select_variables_with_value_by_component_project(link2.id_component_src, id_project)

            for obj in object_property_list:
                text = ""
                if len(variables_list) > 0:
                    position = len(variables_list)

                    for var in variables_list:
                        position -= 1
                        text += var.var_name

                        if position >= 2:
                            text += ", "
                        elif position >= 1:
                            text += " or "

                if obj.replace("-", " ") == "delayed" and cp != None:
                        cause = "Temporary obstruction does not allow the reading of the " + cp.name + " by " + link2.name_dst + "."
                        req = "The feedback from " + cp.name + " to " + link2.name_dst + " must have alternative link."
                        result.append(Loss_Scenery(side, causal_factor_name + " by " + cp.name, cp.name, cause, req, controller.id, cp.id, link2.id_component_src, link2.id_component_dst))

                if (obj.replace("-", " ") == "inadequate" or obj.replace("-", " ") == "missing") and cp != None:
                        cause = "Feedback of " + cp.name + " to " + link2.name_dst
                        if text != "":
                            cause += " (" + text + ")"
                        cause += " is " + obj.replace("-", " ") + "."
                        req = "The communication from " + cp.name + " to " + link2.name_dst + " must be improved."
                        result.append(Loss_Scenery(side, causal_factor_name + " by " + cp.name, cp.name, cause, req, controller.id, cp.id, link2.id_component_src, link2.id_component_dst))

        return result

    if causal_factor_name == Constant.FEEDBACK_OF_CONTROLLER:
        list_controllers = DB_Components.select_component_by_thing_project_exceptId(Constant.DB_ID_CONTROLLER, id_project, controller.id)

        for ctl in list_controllers:
            comp_list_cp = DB_Components_Links.select_component_links_by_project_and_thing_and_controller(id_project, Constant.DB_ID_CONTROLLER, controller.id, False)
            for link2 in comp_list_cp:
                if ctl.id == link2.id_component_src:
                    variables_list = DB_Variables.select_variables_with_value_by_controller_project_link(link2.id_component_dst, id_project, link2.id)

                    if len(variables_list) > 0:
                        for obj in object_property_list:
                            text = ""
                            if len(variables_list) > 0:
                                position = len(variables_list)

                                for var in variables_list:
                                    position -= 1
                                    text += var.var_name

                                    if position >= 2:
                                        text += ", "
                                    elif position >= 1:
                                        text += " or "

                            if obj.replace("-", " ") == "delayed":
                                cause = "Feedback"
                                if text != "":
                                    cause += " (" + text + ")"
                                cause += " from " + ctl.name + " to " + controller.name + " is delayed."
                                req = "The feedback from " + ctl.name + " to " + controller.name + " must have alternative link."
                                result.append(Loss_Scenery(side, causal_factor_name + " by " + ctl.name, ctl.name, cause, req, controller.id, ctl.id, ctl.id, controller.id, ctl.name, controller.name))

                            elif obj.replace("-", " ") == "missing":
                                cause = "Feedback from " + ctl.name + " to " + controller.name
                                if text != "":
                                    cause += " (" + text + ")"
                                cause += " is " + obj.replace("-", " ") + "."
                                req = "The communication from " + ctl.name + " to " + controller.name + " must be improved."
                                result.append(Loss_Scenery(side, causal_factor_name + " by " + ctl.name, ctl.name, cause, req, controller.id, ctl.id, ctl.id, controller.id, ctl.name, controller.name))

        return result

    if causal_factor_name == Constant.PROCESS_MODEL:
        cp = DB_Components.select_one_component_by_thing_project_analysis(Constant.DB_ID_CP, id_project)
        ec = DB_Components.select_component_by_project_father_thing(id_project, controller.id, Constant.DB_ID_EXT_INFORMATION)
        comp_list = DB_Components.select_component_by_project_father_thing(id_project, controller.id, Constant.DB_ID_PROCESS_MODEL)

        if cp != None:
            for pm in comp_list:
                for obj in object_property_list:
                    cause = "Current state of " + pm.name + " is " + obj.replace("-", " ") + "."

                    if obj.replace("-", " ") == "wrong":
                        req = "The process model of " + controller.name + " must represent the " + cp.name + "."
                        result.append(Loss_Scenery(side, causal_factor_name, pm.name, cause, req, controller.id, pm.id, pm.id, controller.id, pm.name, controller.name))
        return result

    if causal_factor_name == Constant.INPUT:
        cp = DB_Components.select_one_component_by_thing_project_analysis(Constant.DB_ID_CP, id_project)

        if cp == None:
            return result

        list_controlled_process_input = DB_Components.select_component_by_project_father_thing(id_project, cp.id, Constant.DB_ID_INPUT)

        if len(list_controlled_process_input) > 0:
            input = list_controlled_process_input[0]

            list_controlled_process_input_variables = DB_Variables.select_variables_by_component_project(input.id, id_project)

            if len(list_controlled_process_input_variables) > 0:
                variables_list = DB_Variables_Values.select_values_by_variable(list_controlled_process_input_variables[0].id)

                for obj in object_property_list:
                    text = ""
                    position = len(variables_list)
                    for val in variables_list:
                        position -= 1
                        text += val.value

                        if position >= 2:
                            text += ", "
                        elif position >= 1:
                            text += " or "

                    cause = input.name
                    if text != "":
                        cause += " (" + text + ")"
                    cause += " is " + obj.replace("-", " ") + "."

                    if (obj.replace("-", " ") == "missing" or obj.replace("-", " ") == "wrong") and cp != None:
                        req = "The " + cp.name + " must support the input == " + input.name + "."
                        result.append(Loss_Scenery(side, causal_factor_name, input.name, cause, req, controller.id, input.id, input.id, cp.id, input.name, cp.name))

        return result

    if causal_factor_name == Constant.SENSOR:
        comp_list = DB_Components_Links.select_component_links_by_project_and_thing_and_controller(id_project, Constant.DB_ID_SENSOR, controller.id, False)
        cp = DB_Components.select_one_component_by_thing_project_analysis(Constant.DB_ID_CP, id_project)

        for comp in comp_list:
            sensor = DB_Components.select_component_by_id(comp.id_component_src)

            variables_list = DB_Variables.select_variables_with_value_by_controller_project_link(comp.id_component_dst, id_project, comp.id)
            if len(variables_list) > 0:
                    var_text = ""
                    if len(variables_list) > 0:
                        position = len(variables_list)
                        for var in variables_list:
                            position -= 1
                            var_text += var.var_name
                            if position >= 2:
                                var_text += ", "
                            elif position >= 1:
                                var_text += " or "


            for obj in object_property_list:
                if obj.replace("-", " ") == "delayed":
                    if cp != None:
                        cause = "Temporary obstruction does not allow the reading of the " + cp.name + " by " + sensor.name + "."
                        req = "The " + sensor.name + " shall have alternative way to read " + cp.name + "."
                        result.append(Loss_Scenery(side, causal_factor_name, sensor.name, cause, req, controller.id, sensor.id, sensor.id, controller.id, sensor.name, controller.name))

                    cause = "Feedback ("+ var_text +") delays between " + sensor.name + " and " + controller.name + "."
                    req = "The communication of " + sensor.name + " to " + controller.name + " must be improved."
                    result.append(Loss_Scenery(side, causal_factor_name, sensor.name, cause, req, controller.id, sensor.id, sensor.id, controller.id, sensor.name, controller.name))

                if obj.replace("-", " ") == "wrong" and cp != None:
                    cause = "Current state of the " + cp.name+ " cannot be read accurately by " + sensor.name + "."
                    req = "The " + sensor.name + " must have accuracy == 0.0x."
                    result.append(Loss_Scenery(side, causal_factor_name, sensor.name, cause, req, controller.id, sensor.id, sensor.id, controller.id, sensor.name, controller.name))

                if obj.replace("-", " ") == "missing":
                    if cp != None:
                        cause = "Feedback of " + sensor.name + " is missing (" + obj.replace("-", " ") + ")."
                        req = "The " + sensor.name + " must be maintained when time of use == x."
                        result.append(Loss_Scenery(side, causal_factor_name, sensor.name, cause, req, controller.id, sensor.id, sensor.id, controller.id, sensor.name, controller.name))

                    cause = "Feedback ("+ var_text +") lost or corrupted."
                    req = "Communication of " + sensor.name + " to " + controller.name + " must be improved."
                    result.append(Loss_Scenery(side, causal_factor_name, sensor.name, cause, req, controller.id, sensor.id, sensor.id, controller.id, sensor.name, controller.name))

                if obj.replace("-", " ") == "failure" and cp != None:
                    cause = cp.name + " cannot be read (" + obj.replace("-", " ") + ") by the " + sensor.name + "."
                    req = "The " + sensor.name + " must be maintained when time of use == x."
                    result.append(Loss_Scenery(side, causal_factor_name, sensor.name, cause, req, controller.id, sensor.id, sensor.id, controller.id, sensor.name, controller.name))

        return result

    if causal_factor_name == Constant.CONTROL_ACTION_HLC_CP:
        list_controllers = DB_Components.select_component_by_thing_project_exceptId(Constant.DB_ID_CONTROLLER, id_project, controller.id)

        for ctl in list_controllers:
            cp = DB_Components.select_one_component_by_thing_project_analysis(Constant.DB_ID_CP, id_project)
            comp_list = DB_Components_Links.select_component_links_by_project_and_thing_and_controller(id_project, Constant.DB_ID_CP, ctl.id, True)

            if cp == None:
                return result

            for comp in comp_list:
                actions_list = DB_Actions_Components.select_actions_by_component_and_project(comp.id_component_src, id_project)

                for obj in object_property_list:
                    if len(actions_list) > 0:
                        text = ""
                        position = len(actions_list)

                        for act in actions_list:
                            position -= 1
                            text += act.name

                            if position >= 2:
                                text += ", "
                            elif position >= 1:
                                text += " or "

                        cause = ctl.name + " issues a control action (" + text + ") that conflicts with the one provided by the " + controller.name + "."

                        if obj.replace("-", " ") == "conflicting":
                            req = "The " + ctl.name + " must have conflict analysis for control actions."
                            result.append(Loss_Scenery(side, causal_factor_name, ctl.name, cause, req, controller.id, ctl.id, ctl.id, cp.id, ctl.name, cp.name))
        return result

    if causal_factor_name == Constant.CONTROL_ACTION_HLC_CONTROLLER:
        cp = DB_Components.select_one_component_by_thing_project_analysis(Constant.DB_ID_CP, id_project)
        comp_list = DB_Components_Links.select_component_links_by_project_and_thing_and_controller_CA_ONLY(id_project, Constant.DB_ID_CONTROLLER, controller.id, True)

        for comp in comp_list:
            actions_list = DB_Actions_Components.select_actions_by_component_and_project_and_destiny(comp.id_component_src, id_project, comp.id_component_dst)

            for obj in object_property_list:
                if len(actions_list) > 0:
                    text = ""
                    position = len(actions_list)

                    for act in actions_list:
                        position -= 1
                        text += act.name

                        if position >= 2:
                            text += ", "
                        elif position >= 1:
                            text += " or "

                    if obj.replace("-", " ") == "inappropriate" and cp != None:
                        cause = controller.name + " issued an incorrect (" + obj.replace("-", " ") + ") control action: " + text + "; to " + comp.name_dst + "."
                        req = "The process model in " + controller.name + " must represent the " + cp.name + " and " + comp.name_dst + "."
                        result.append(Loss_Scenery(side, causal_factor_name, comp.name_dst, cause, req, controller.id, controller.id, comp.id_component_src, comp.id_component_dst, comp.name_src, comp.name_dst))

                    if obj.replace("-", " ") == "missing":
                        cause = controller.name + " does not provide (" + obj.replace("-", " ") + ") the control action: " + text + "; to " + comp.name_dst + "."
                        req = "The communication of " + controller.name + " to " + comp.name_dst + " must be improved."
                        result.append(Loss_Scenery(side, causal_factor_name, comp.name_dst, cause, req, controller.id, controller.id, comp.id_component_src, comp.id_component_dst, comp.name_src, comp.name_dst))
                        # correct ^
                        cause = comp.name_dst + " does not provide the received control action (" + text + ") from " + controller.name + "."
                        req = "The " + comp.name_dst + " must have ongoing analysis after system modification."
                        result.append(Loss_Scenery(side, causal_factor_name, comp.name_dst, cause, req, controller.id, comp.id_component_dst, comp.id_component_src, comp.id_component_dst, comp.name_src, comp.name_dst))

                    if obj.replace("-", " ") == "conflicting" and cp != None:
                        cause = controller.name + " issued an conflicting control action: " + text + "; to " + comp.name_dst + "."
                        req = "The process model in " + controller.name + " must represent the " + cp.name + " and " + comp.name_dst + "."
                        result.append(Loss_Scenery(side, causal_factor_name, comp.name_dst, cause, req, controller.id, controller.id, comp.id_component_src, comp.id_component_dst, comp.name_src, comp.name_dst))
#(side, onto_name, component, causes, requirement, id_controller, id_component, id_component_src, id_component_dst, name_src = "", name_dst = "", mechanism = ""):
        return result

    # print(causal_factor_name + " is not identified.")
    return result

# Creates a specific list of causal factor and context
def create_UCA_list(individual_list, analysis_file, counter):

    result_list = []
    control_actions_list = []
    context_list = []

    for thing in individual_list:
        if "Control_action_" in thing:
            control_actions_list.append(thing)
        else:
            context_list.append(thing)

    for action in control_actions_list:
        aux_actions_list = Dictionary.get_list(action)
        if len(aux_actions_list) > 0:
            new_counter = counter + len(result_list)
            result_list.extend(create_UCA_list_context(aux_actions_list, context_list, analysis_file, new_counter))

    return result_list

# Secondary function of create_UCA_list
def create_UCA_list_context(aux_actions_list, context_list, analysis_file, counter):
    result_list = []
    uca_list = Dictionary.get_list(Constant.UCA_TYPE)

    for control_action in aux_actions_list:
        for aux_uca in uca_list:
            for context in context_list:
                aux_context_list = Dictionary.get_list(context)
                for element in aux_context_list:
                    counter+=1
                    requirement = str(counter) + " >> " + control_action + " is " + aux_uca + " when " + element + "\n"
                    analysis_file.write(requirement)

                    aux_things_list = [control_action, element]
                    req_obj = Requirement(counter, Constant.SAFETY, requirement, aux_things_list)
                    result_list.append(req_obj)



    return result_list



# # Creates the main list of causal factor
# def get_causal_factor_list(causal_factor_name, name, id_project, controller, object_property_list):
#     new_line = False
#     result = []
#
#     if causal_factor_name == Constant.ACTUATOR:
#         cp = DB_Components.select_one_component_by_thing_project_analysis(Constant.DB_ID_CP, id_project)
#
#         comp_list = DB_Components_Links.select_component_links_by_project_and_thing_and_controller(id_project, Constant.DB_ID_ACTUATOR, controller.id, True)
#
#         for comp in comp_list:
#             actuator = DB_Components.select_component_by_id(comp.id_component_dst)
#             result.append("The " + actuator.name + " does not perform their function.")
#             # result.append("The " + actuator.name + " does not execute the Control Action.")
#             result.append("The " + actuator.name + " cannot act in " + cp.name + ".")
#             # result.append("The " + actuator.name + " delays to enforce the Control Action.")
#             # result.append(actuator.name + " performs a non-issued Control Action.")
#
#         return result
#
#     if causal_factor_name == Constant.ALGORITHM:
#         result.append(name + " is an inadequate control algorithm.")
#         result.append(name + " is an incorrect algorithm was designed.")
#         result.append(name + " is ineffective, unsafe or incomplete after process changes.")
#         result.append(name + " was updated incorrectly.")
#         return result
#
#     if causal_factor_name == Constant.CONTROL_ACTION_ACTUATOR:
#         cp = DB_Components.select_one_component_by_thing_project_analysis(Constant.DB_ID_CP, id_project)
#
#         comp_list = DB_Components_Links.select_component_links_by_project_and_thing_and_controller(id_project, Constant.DB_ID_ACTUATOR, controller.id, True)
#
#         result.append("The " + controller.name + " does not perform their function.")
#
#         for comp in comp_list:
#             actions_list = DB_Actions_Components.select_actions_by_component_and_project(comp.id_component_src, id_project)
#             actuator = DB_Components.select_component_by_id(comp.id_component_dst)
#
#             for act in actions_list:
#                 result.append(controller.name + " does not provide the Control Action (" + act.name + ") to " + actuator.name + ".")
#                 result.append(controller.name + " issued an incorrect Control Action (" + act.name + ") to " + actuator.name + ".")
#                 result.append(actuator.name + " delays to be enforced by the the issued Control Action (" + act.name + ").")
#                 # result.append(actuator.name + " does not execute the the issued Control Action (" + act.name + ").")
#                 result.append(actuator.name + " performs a non-issued Control Action (" + act.name + ").")
#
#         return result
#
#     if causal_factor_name == Constant.CONTROL_ACTION_CP:
#         cp = DB_Components.select_one_component_by_thing_project_analysis(Constant.DB_ID_CP, id_project)
#         comp_list = DB_Components_Links.select_component_links_by_project_and_thing_and_controller(id_project, Constant.DB_ID_CONTROLLER, controller.id, True)
#
#         for comp in comp_list:
#             actions_list = DB_Actions_Components.select_actions_by_component_and_project(comp.id_component_src, id_project)
#             result.append("The " + controller.name + " does not perform their function.")
#
#             for act in actions_list:
#                 result.append(controller.name + " does not provide the Control Action (" + act.name + ") or issued an incorrect.")
#                 result.append(controller.name + " cannot act in " + cp.name + " or complete the execution of Control Action (" + act.name + ").")
#                 result.append(controller.name + " performs a non-issued Control Action (" + act.name + ").")
#                 result.append("The issued Control Action (" + act.name + ") delays to be enforced by the " + controller.name + ".")
#
#
#         return result
#
#     if causal_factor_name == Constant.CONTROLLER:
#         result.append("The " + controller.name + " does not perform their function.")
#
#
#         return result
#
#
#     if causal_factor_name == Constant.EXTERNAL_INFORMATION:
#         link_list = DB_Components_Links.select_component_links_by_project_and_thing(id_project, Constant.DB_ID_EXT_INFORMATION, True)
#
#         for link in link_list:
#             variables_list = DB_Variables.select_variables_with_value_by_component_project(link.id_component_src, id_project)
#
#             if len(variables_list) > 0:
#                 # text = ""
#                 # position = len(variables_list)
#
#                 for var in variables_list:
#                     result.append(name + " sends the wrong value of " + var.var_name + ".")
#                     result.append(name + " missing the value " + var.var_name + ".")
#                 #     position -= 1
#                 #     text += var.var_name
#                 #
#                 #     if position >= 2:
#                 #         text += ", "
#                 #     elif position >= 1:
#                 #         text += " and "
#                 #
#                 # result.append(name + " sends the wrong value of " + text + ".")
#                 # result.append(name + " missing the value " + text + ".")
#         return result
#
#     if causal_factor_name == Constant.ENVIRONMENTAL_DISTURBANCES:
#         cp_list = DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_CP, id_project)
#         env_dist_list = DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_ENV_DISTURBANCES, id_project)
#
#         for cp in cp_list:
#             for env_dist in env_dist_list:
#                 result.append(cp.name + " affected by natural or man made " + env_dist.name)
#
#         return result
#
#     if causal_factor_name == Constant.FEEDBACK_OF_CP:
#
#         link_list = DB_Components_Links.select_component_links_by_project_and_thing(id_project, Constant.DB_ID_SENSOR, True)
#
#         for link in link_list:
#             variables_list = DB_Variables.select_variables_with_value_by_component_project(link.id_component_src, id_project)
#
#             if len(variables_list) > 0:
#                 for var in variables_list:
#                     # result.append(name + " sends the wrong value of " + var.var_name + ".")
#                     # result.append(name + " missing the value " + var.var_name + ".")
#                     result.append(name + " (" + var.var_name + ") has measurement inaccuracies.")
#                     result.append(name + " (" + var.var_name + ") is missing.")
#
#         return result
#
#     if causal_factor_name == Constant.PROCESS_MODEL:
#         result.append(name + " Current state of the " + name + " is inconsistent.")
#         result.append(name + " Current state of the " + name + " is incorrect.")
#         result.append(name + " Current state of the " + name + " is incomplete.")
#         return result
#
#     if causal_factor_name == Constant.INPUT:
#         input = DB_Components.select_one_component_by_thing_project_analysis(Constant.DB_ID_INPUT, id_project)
#         variables_list = DB_Variables.select_variables_with_value_by_component_project(input.id, id_project)
#
#         if len(variables_list) > 0:
#             for var in variables_list:
#                 for val in var.values_list:
#                     result.append(val.value + " is a missing or inadequate of " + input.name + ".")
#         else:
#             result.append("Missing or inadequate " + input.name + ".")
#
#         return result
#
#     if causal_factor_name == Constant.SENSOR:
#         cp = DB_Components.select_one_component_by_thing_project_analysis(Constant.DB_ID_CP, id_project)
#
#         comp_list = DB_Components_Links.select_component_links_by_project_and_thing_and_controller(id_project, Constant.DB_ID_SENSOR, controller.id, False)
#
#         for comp in comp_list:
#             sensor = DB_Components.select_component_by_id(comp.id_component_src)
#             result.append("The " + comp.name_src + " does not perform their function.")
#             result.append("The " + comp.name_src + " delays to send feedback to " + controller.name + ".")
#             result.append("The " + comp.name_src + " sends the wrong feedback to " + controller.name + ".")
#             result.append("The " + comp.name_src + " can not read the " + cp.name + ".")
#
#         return result
#     # if causal_factor_name == Constant.CONTROL_ACTION_HLC_CONTROLLER:
#     # to do
#
#     # if causal_factor_name == Constant.CONTROL_ACTION_HLC_CP:
#     # to do
#
#     result.append(causal_factor_name + "(" + name + ") is not identified.")
#     return result
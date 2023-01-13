from owlready2 import *

import Constant
from Objects.Conflict.Conflict import Conflict
from Objects.Hierarchy import Hierarchy
from Objects.Relation import Relation


# function to show all ontology classes
def show_ontology_all_class():
    for Class in Thing.subclasses():
        print("CLASS: " + Class.name)
        show_ontology_all_subclass(Class.iri, " ")

# function to show all the subclasses
def show_ontology_all_subclass(iri, tab):
    Class = IRIS[iri]
    next_tab = tab + "    "

    for SuperClass in Class.is_a:
       if isinstance(SuperClass, ThingClass):
           print(next_tab + "Is instance: " + SuperClass.name + ". IRI: " + SuperClass.iri)


    for EquivClass in Class.equivalent_to:
        print(next_tab + "Equivalent class: " + EquivClass.iri)

    for SubClass in Class.subclasses():
        print(next_tab + "Subclass: " + SubClass.name + ". IRI: " + SubClass.iri)
        show_ontology_all_subclass(SubClass.iri, next_tab)

    for individual in Class.instances():
        print(next_tab + "Individual: " + individual.name + ". IRI: " + individual.iri)

# get the subclasses of an IRI
def get_all_subclass(iri):
    Class = IRIS[iri]
    list_of_relations = []

    for SubClass in Class.subclasses():
        list_of_result = get_all_subclass(SubClass.iri)
        list_of_relations.append(Relation(SubClass, list_of_result))

    return list_of_relations

def get_subclass_first_level(onto, name_class):
        list_of_subclass = []
        name_found = find_one_ontology_class(onto, name_class)
        try:
            if name_found is None:
                print("ERROR to find the name: " + name_class + ". Stopping this process...")
                return list_of_subclass

            Class = IRIS[name_found.iri]
            aux = Class.subclasses()
            for SubClass in Class.subclasses():
                list_of_subclass.append(SubClass.name)

        except NameError as e:
            print(e)
        return list_of_subclass

# Function to find a specific class name, if the name doesn't existe return NONE
def find_one_ontology_class(onto, name):
    for c in onto.search(iri = "*" + name + "*", _case_sensitive=True):
        # print("RESULT: " + str(c))
        if c.name == name:
            return c
    return None

# Function to find a specific class name, if the name doesn't existe return NONE
def find_all_ontology_class(onto, name):
    list = []
    for c in onto.search(iri = "*" + name + "*", _case_sensitive=True):
        # print("RESULT: " + str(c))
        if name in c.name:
            list.append(c.name)
    return list

# find the sons of a class, returns a Relation object
def list_relations(onto, name_class):
    name_found = find_one_ontology_class(onto, name_class)

    if name_found is None:
        print("ERROR to find the name: " + name_class + ". Stopping this process...")
        return None

    relation = Relation(name_found, get_all_subclass(name_found.iri))
    print("Work done for " + name_class)
    return relation

# find the sons of a class, returns a Relation object
def list_subclass_with_property(onto, name_class, name_property):
    name_found = find_one_ontology_class(onto, name_class)
    filtered_list = []

    if name_found is None:
        print("ERROR to find the name: " + name_class + ". Stopping this process...")
        return []

    relation_list = get_all_subclass(name_found.iri)
    filtered_list = get_subclass_first_level(onto, name_class)
    filtered_list.extend(get_all_subclass_with_property(relation_list, name_property))
    print("Work done for " + name_class)
    return filtered_list

def get_all_subclass_with_property(relation_list, name_property):
    list_of_relations = []
    for relation in relation_list:
        list_of_result = get_all_subclass_with_property(relation.son_class, name_property)
        for ff in relation.son_class:
            for obj in ff.parent_class.is_a:
                if isinstance(obj, Restriction):
                    if obj.property.name == name_property:
                        list_of_relations.append(ff.parent_class.name)

    return list_of_relations

# find the sons of a class, returns a Relation object
def list_relations_for_link(onto, name_to_find):
    name_found = find_one_ontology_class(onto, Constant.LINK)

    if name_found is None:
        print("ERROR to find the name: the Link classes. Stopping this process...")
        return None

    Class = IRIS[name_found.iri]
    list_of_relations = []

    for SubClass in Class.subclasses():
        list_class, list_individuals = find_in_subclass(SubClass.iri, SubClass.name, name_to_find)

        if len(list_class) > 0:
            list_of_relations.append(Relation(SubClass, list_class, list_individuals))

    relation = Relation(Class, list_of_relations)

    return relation

# get the subclasses of an IRI
def find_in_subclass(iri, subclass_name, name_to_find):
    Class = IRIS[iri]
    list_of_relations = []
    list_of_individuals = []
    name_found = False

    for SubClass in Class.subclasses():
        list_of_relations.append(Relation(SubClass, []))

    for individual in Class.instances():
        if individual.name == name_to_find:
            name_found = True
        list_of_individuals.append(individual.name)

    list_of_individuals.remove(subclass_name)

    if not name_found:
        list_of_relations = []
        list_of_individuals = []

    return list_of_relations, list_of_individuals

# main function to print lists
def print_relation(relation):
    print("Name: " + str(relation.parent_class.name))
    print_relation_list(relation.son_class)

# secondary function to print the sublists
def print_relation_list(list):
    for relation in list:
        print("Son: " + str(relation.parent_class.name))# + " --> IRI: " + str(relation.parent_class.iri))
        print_relation_list(relation.son_class)

# find the sons of a class, returns a Relation object
def find_individuals_of_class(onto, name_class):
    name_found = find_one_ontology_class(onto, name_class)
    hierarchy = None
    try:
        if name_found is None:
            print("ERROR to find the name: " + name_class + ". Stopping this process...")
            return None

        Class = IRIS[name_found.iri]
        list_of_individuals = []
        name_list = []

        for individual in Class.instances():
            list_of_individuals.append(individual)
            name_list.append(individual.name)

        hierarchy = Hierarchy(Class, list_of_individuals, name_list)
    except NameError as e:
        print(e)
    # print("Work done for " + name_class)
    return hierarchy

# find the sons of a class, returns a Relation object
def find_individuals_of_class_filtering(onto, name_class, filter):
    name_found = find_one_ontology_class(onto, name_class)

    if name_found is None:
        print("ERROR to find the name: " + name_class + ". Stopping this process...")
        return None

    Class = IRIS[name_found.iri]
    list_of_individuals = []
    name_list = []

    for individual in Class.instances():
        if filter in individual.name:
            list_of_individuals.append(individual)
            name_list.append(individual.name)

    hierarchy = Hierarchy(Class, list_of_individuals, name_list)
    # print("Work done for " + name_class)
    return hierarchy

def find_individuals_of_class_return_idThing(onto, name_class, filter):
    name_found = find_one_ontology_class(onto, name_class)

    if name_found is None:
        print("ERROR to find the name: " + name_class + ". Stopping this process...")
        return None

    Class = IRIS[name_found.iri]
    id_list = []

    for individual in Class.instances():
        if filter in individual.name:
            id_aux = find_id_thing(individual.name.replace(filter, ""))
            if id_aux != "":
                id_list.append(find_id_thing(individual.name.replace(filter, "")))
    return id_list

# find the sons of a class, returns a Relation object
def find_id_thing(to_find):
    if to_find.lower() == Constant.ACTUATOR.lower():
        return Constant.DB_ID_ACTUATOR

    if to_find.lower() == Constant.CONTROLLED_PROCESS.lower():
        return Constant.DB_ID_CP

    if to_find.lower() == Constant.HIGH_LEVEL_CONTROLLER.lower():
        return Constant.DB_ID_CONTROLLER

    if to_find.lower() == Constant.SENSOR.lower():
        return Constant.DB_ID_SENSOR

    if to_find.lower() == Constant.CONTROLLER.lower():
        return Constant.DB_ID_CONTROLLER

    if to_find.lower() == Constant.INPUT.lower():
        return Constant.DB_ID_OUTPUT

    if to_find.lower() == Constant.EXTERNAL_INFORMATION.lower():
        return Constant.DB_ID_EXT_INFORMATION

    if to_find.lower() == Constant.ENVIRONMENTAL_DISTURBANCES.lower():
        return Constant.DB_ID_ENV_DISTURBANCES

    return ""

# TO DELETE
def compare_and_generate_safety_security(safety_list, security_list):
    date_now = datetime.datetime.now()
    analysis_file = open(Constant.ANALYSIS_PATH + "relations_analysis_" + str(date_now.year) + "-" + str(date_now.month) + "-" + str(date_now.day) + ".txt", "w")
    for safety in safety_list:
        analysis_file.write(safety.requirement)
        for thing in safety.elements_list:
            find_for_security_requirements(thing, security_list, safety.requirement, analysis_file)
        analysis_file.write("\n")

    analysis_file.close()

# TO DELETE
def find_for_security_requirements(saf_thing, security_list, safety, analysis_file):
    result_list = []

    for security in security_list:
        for sec_thing in security.elements_list:
            if saf_thing == sec_thing:
                result_list.append(security.id)
    analysis_file.write(saf_thing + " is related with Security requirement:  " + str(result_list) + "\n")

def get_property_list_ontology(onto, name_source, name_destiny):
    name = find_individuals_of_class(onto, name_source)
    result_list = []

    try:
        if name != None:
            # print("Name source: " + name_source)
            for obj in name.class_parent.is_a:
                if isinstance(obj, Restriction):
                    if obj.value.name == name_destiny:
                        aux_string = str(obj.property.name)
                        aux_string = aux_string.replace("saf_", "")
                        for slice in aux_string.split("_"):
                            result_list.append(slice)
        else:
            print("Error: " + name_source)

    except NameError as e:
        print(e)

    return result_list

# discover if an IRI has a rpoperty with destiny to a specific class
def find_property_by_name_object(onto, name_source, name_destiny, name_object):
    try:
        # name_class = IRIS[iri]
        name = find_individuals_of_class(onto, name_source)

        if name != None:
            # print("Name source: " + name_source)

            tt = name.class_parent.is_a

            for obj in name.class_parent.is_a:
                if isinstance(obj, Restriction):
                    if obj.property.name == name_object:
                        if obj.value.name == name_destiny:
                            return True
        else:
            print("Error: " + name_source)

    except NameError as e:
        print(e)

    return False

def class_has_son(onto, is_component, name_class, name_son, property):
    try:
        # find for component first
        name_class = find_individuals_of_class(onto, name_class)
        if name_class != None:

            if is_component:
                for obj in name_class.name_list:
                    if obj == name_son:

                        if obj == Constant.CONTROLLED_PROCESS:
                            son_class = get_class(onto, Constant.CONTROLLED_PROCESS_full_name)
                        else:
                            son_class = get_class(onto, obj)

                        if son_class != None:
                            for obj_s in son_class.is_a:
                                if isinstance(obj_s, Restriction):
                                    p = obj_s.property.name
                                    if p == property:
                                        return True
            else:
                for obj in name_class.name_list:
                    if obj.lower() == name_son:
                        son_class = get_class(onto, obj)

                        if son_class != None:
                            for obj_s in son_class.is_a:
                                if isinstance(obj_s, Restriction):
                                    p = obj_s.property.name
                                    if p == property:
                                        return True
    except NameError as e:
        print(e)

    return False

# find the sons of a class, returns a Relation object
def get_class(onto, name_class):
    name_found = find_one_ontology_class(onto, name_class)

    if name_found is None:
        print("ERROR to find the name: " + name_class + ". Stopping this process...")
        return None

    return IRIS[name_found.iri]

# find the conflict links of a classes
def find_for_object_property_of_class(onto, name_class, name_of_property):
    list_of_conflicts = []
    name_found = find_one_ontology_class(onto, name_class)
    try:
        if name_found is None:
            print("ERROR to find the name: " + name_class + ". Stopping this process...")
            return list_of_conflicts

        Class = IRIS[name_found.iri]
        for obj in Class.is_a:
            if isinstance(obj, Restriction):
                if obj.property.name == name_of_property:
                    list_of_conflicts.append(obj.value.name)
    except NameError as e:
        print(e)
    return list_of_conflicts

# Find all subclasses of a class
def find_safety_security_only_subclass(onto, name_to_find):
    concepts = []
    try:
        name_found = find_one_ontology_class(onto, name_to_find)
        if name_found is None:
            print("ERROR to find the name: " + name_to_find + ". Stopping this process...")
            return concepts

        Class = IRIS[name_found.iri]

        for SubClass in Class.subclasses():
            concepts.append(Conflict(SubClass.name.replace("_", " "), [], False, SubClass))
            # concepts.append(SubClass.name.replace("_", " "))
    except NameError as e:
        print(e)
    return concepts

# find class by the conflict links of a classes
def find_class_for_object_property_of_class(onto, name_class, name_of_property):
    list_of_conflicts = []
    name_found = find_one_ontology_class(onto, name_class)
    try:
        if name_found is None:
            print("ERROR to find the name: " + name_class + ". Stopping this process...")
            return list_of_conflicts

        Class = IRIS[name_found.iri]
        for obj in Class.is_a:
            if isinstance(obj, Restriction):
                if obj.property.name == name_of_property:
                    list_of_conflicts.append(obj.value)
    except NameError as e:
        print(e)
    return list_of_conflicts

def find_safety_security_conflicts_subclass(onto):
    conflicts = []
    try:
        name_found = find_one_ontology_class(onto, Constant.SAF_CONFLICT_REINFORCEMENT_RECOMMENDATION)
        if name_found is None:
            print("ERROR to find the name: " + Constant.SAF_CONFLICT_REINFORCEMENT_RECOMMENDATION + ". Stopping this process...")
            return conflicts

        Class = IRIS[name_found.iri]
        list_of_conflicts = []

        for SubClass in Class.subclasses():
            list_of_conflicts = load_for_object_property_of_class(SubClass, Constant.IS_SAF_SEC_CONFLICT)
            conflicts.append(Conflict(SubClass.name.replace("_", " "), list_of_conflicts, False, SubClass))
    except NameError as e:
        print(e)
    return conflicts

def find_safety_security_reinforcements_subclass(onto):
    reinforcements = []
    try:
        name_found = find_one_ontology_class(onto, Constant.SAF_CONFLICT_REINFORCEMENT_RECOMMENDATION)
        if name_found is None:
            print("ERROR to find the name: " + Constant.SAF_CONFLICT_REINFORCEMENT_RECOMMENDATION + ". Stopping this process...")
            return reinforcements

        Class = IRIS[name_found.iri]
        list_of_reinforcements = []

        for SubClass in Class.subclasses():
            list_of_reinforcements = load_for_object_property_of_class(SubClass, Constant.IS_SAF_SEC_REINFORCEMENT)
            # if len(list_of_reinforcements) > 0:
            reinforcements.append(Conflict(SubClass.name.replace("_", " "), list_of_reinforcements, False, SubClass))
    except NameError as e:
        print(e)
    return reinforcements

# load all relations, except....
def find_safety_security_conflicts_subclass_EXCEPTION(onto, saf_except, sec_except, relation):
    conflicts = []
    try:
        name_found = find_one_ontology_class(onto, Constant.SAF_CONFLICT_REINFORCEMENT_RECOMMENDATION)
        if name_found is None:
            print("ERROR to find the name: " + Constant.SAF_CONFLICT_REINFORCEMENT_RECOMMENDATION + ". Stopping this process...")
            return conflicts

        Class = IRIS[name_found.iri]

        for SubClass in Class.subclasses():
            exception = ""
            if saf_except == SubClass.name:
                exception = sec_except
            list_of_conflicts = load_for_object_property_of_class_EXCEPTION(SubClass, relation, exception)
            conflicts.append(Conflict(SubClass.name.replace("_", " "), list_of_conflicts, False, SubClass))
    except NameError as e:
        print(e)
    return conflicts

def load_for_object_property_of_class(thing_class, name_of_property):
    list_of_conflicts = []
    try:
        for obj in thing_class.is_a:
            if isinstance(obj, Restriction):
                if obj.property.name == name_of_property:
                    list_of_conflicts.append(obj.value.name.replace("_", " "))
    except NameError as e:
        print(e)
    list_of_conflicts.sort()
    return list_of_conflicts

# load with the exception
def load_for_object_property_of_class_EXCEPTION(thing_class, name_of_property, exception):
    list_of_conflicts = []
    try:
        for obj in thing_class.is_a:
            if isinstance(obj, Restriction):
                if obj.property.name == name_of_property:
                    if exception != "" and obj.value.name == exception:
                        continue
                    else:
                        list_of_conflicts.append(obj.value)
    except NameError as e:
        print(e)
    return list_of_conflicts

# find the conflict links of two classes
def find_object_property_between_two_class(onto, first_class, second_class, name_of_property):
    first_found = find_one_ontology_class(onto, first_class)
    second_found = find_one_ontology_class(onto, second_class)
    try:
        if first_found is None:
            print("ERROR to find the name: " + first_class + ". Stopping this process...")
            return False

        if second_found is None:
            print("ERROR to find the name: " + second_class + ". Stopping this process...")
            return False

        Class = IRIS[first_found.iri]
        for obj in Class.is_a:
            if isinstance(obj, Restriction):
                if obj.property.name == name_of_property:
                    if obj.value.name == second_class:
                        return True
    except NameError as e:
        print(e)
    return False

def string_is_in_subclass(onto, class_father, class_son):
    try:
        name_found = find_one_ontology_class(onto, class_father)
        if name_found is None:
            print("ERROR to find the name: " + class_father + ". Stopping this process...")
            return False

        Class = IRIS[name_found.iri]

        for SubClass in Class.subclasses():
            # for obj in SubClass.is_a:
            if SubClass.name == class_son:
                return True
            # list_of_conflicts = load_for_object_property_of_class(SubClass, Constant.IS_SAF_SEC_CONFLICT)

    except NameError as e:
        print(e)
    return False
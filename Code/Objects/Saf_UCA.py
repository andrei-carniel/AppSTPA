class Saf_UCA:

    def __init__(self, id, id_controller, name_controller, id_uca_type, description_uca_type, id_action, name_action, context_list = [], hazard_list = [],
                 uca_origin = "", is_hazardous = 0, description = ""):
        self.id = id
        self.id_controller = id_controller
        self.name_controller = name_controller
        self.id_uca_type = id_uca_type
        self.description_uca_type = description_uca_type
        self.id_action = id_action
        self.name_action = name_action
        self.context_list = context_list
        self.hazard_list = hazard_list
        self.uca_origin = uca_origin
        self.is_hazardous = is_hazardous
        self.description = description


class Saf_UCA_Hazard:

    def __init__(self, id, id_uca, id_hazard, hazard_description, hazard_order = 0):
        self.id = id
        self.id_uca = id_uca
        self.id_hazard = id_hazard
        self.hazard_description = hazard_description
        self.hazard_order = hazard_order


class Saf_UCA_Context:

    def __init__(self, id, id_uca, id_variable, variable_name, id_value, variable_value):
        self.id = id
        self.id_uca = id_uca
        self.id_variable = id_variable
        self.variable_name = variable_name
        self.id_value =id_value
        self.variable_value = variable_value


class Saf_UCA_Type:

    def __init__(self, id, description):
        self.id = id  # INTEGER PRIMARY KEY
        self.description = description  # TEXT NOT NULL


class Saf_UCA_Type_Comp:

    def __init__(self, name, list_types, comp = None):
        self.name = name
        self.list_types = list_types
        self.comp = comp
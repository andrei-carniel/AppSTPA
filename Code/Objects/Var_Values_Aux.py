class Var_Values_Aux:

    def __init__(self, var_name, variable, values_list):
        self.var_name = var_name
        self.variable = variable
        self.values_list = values_list

class Var_Values_Comp:

    def __init__(self, var_name, variable, values_list, components_list = None):
        self.var_name = var_name
        self.variable = variable
        self.values_list = values_list
        self.components_list = components_list

class Var_Name_Val:

    def __init__(self, var_name, val_value, var_id, val_id):
        self.var_name = var_name
        self.val_value = val_value
        self.var_id = var_id
        self.val_id = val_id

class Var_Context_list:

    def __init__(self, name, list):
        self.name = name
        self.list = list

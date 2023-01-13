class Component:

    def __init__(self, id, id_thing, id_project, name, begin_date, edited_date, comp_father = 0, is_external_component = 0 , hlc_control = 0, ontology_name="", is_human = 0):
        self.id = id  # INTEGER PRIMARY KEY AUTOINCREMENT
        self.id_thing = id_thing  # INTEGER NOT NULL
        self.id_project = id_project  # INTEGER NOT NULL
        self.name = name  # TEXT NOT NULL
        self.begin_date = begin_date  # TEXT NOT NULL
        self.edited_date = edited_date  # TEXT
        self.comp_father = comp_father
        self.is_external_component = is_external_component
        self.hlc_control = hlc_control
        self.ontology_name = ontology_name # TEXT
        self.is_human = is_human

class Component_small:

    def __init__(self, id, id_thing, name, id_stride_dfd):
        self.id = id
        self.id_thing = id_thing
        self.name = name
        self.id_stride_dfd = id_stride_dfd

class Component_Link:

    def __init__(self, id, id_component_src, id_component_dst, name_src = "", name_dst = ""):
        self.id = id  # INTEGER PRIMARY KEY AUTOINCREMENT
        self.id_component_src = id_component_src  # INTEGER NOT NULL
        self.id_component_dst = id_component_dst  # INTEGER NOT NULL
        self.name_src = name_src  # TEXT
        self.name_dst = name_dst  # TEXT

class Component_Link_Ext:

    def __init__(self, id, id_component_src, id_component_dst, name_src = "", type_src = 0, name_dst = "", type_dst = 0):
        self.id = id  # INTEGER PRIMARY KEY AUTOINCREMENT
        self.id_component_src = id_component_src  # INTEGER NOT NULL
        self.id_component_dst = id_component_dst  # INTEGER NOT NULL
        self.name_src = name_src  # TEXT
        self.type_src = type_src
        self.name_dst = name_dst  # TEXT
        self.type_dst = type_dst

class Component_Link_Onto:

    def __init__(self, id, id_component_src, id_component_dst, name_src = "", name_dst = "", onto_name_src = "", onto_name_dst = ""):
        self.id = id
        self.id_component_src = id_component_src
        self.id_component_dst = id_component_dst
        self.name_src = name_src
        self.name_dst = name_dst
        self.onto_name_src = onto_name_src
        self.onto_name_dst = onto_name_dst

class Component_Link_Var:

    def __init__(self, id, id_link, id_var=0, id_act=0):
        self.id = id
        self.id_link = id_link
        self.id_var = id_var
        self.id_act = id_act

class Component_Link_Var_HLC:

    def __init__(self, id, id_link, id_var, id_act, name_control_action, id_component_src, id_component_dst, name_src, name_dst):
        self.id = id
        self.id_link = id_link
        self.id_var = id_var
        self.id_act = id_act
        self.name_control_action = name_control_action
        self.id_component_src = id_component_src
        self.id_component_dst = id_component_dst
        self.name_src = name_src
        self.name_dst = name_dst

class Component_Link_Stride:

    def __init__(self, id, id_component_src, id_component_dst, name_src = "", name_dst = "", type_src = 0, type_dst = 0, list_act = [],
                 list_var = [], is_ext = False, is_hlc = False, is_bound_trust = 0, id_dfd_src = 0, id_dfd_dst = 0, id_dfd_link = 0, ):
        self.id = id  # INTEGER PRIMARY KEY AUTOINCREMENT
        self.id_component_src = id_component_src  # INTEGER NOT NULL
        self.id_component_dst = id_component_dst  # INTEGER NOT NULL
        self.name_src = name_src  # TEXT
        self.name_dst = name_dst  # TEXT
        self.type_src = type_src
        self.type_dst = type_dst
        self.list_act = list_act
        self.list_var = list_var
        self.is_ext = is_ext
        self.is_hlc = is_hlc
        self.is_bound_trust = is_bound_trust
        self.id_dfd_src = id_dfd_src
        self.id_dfd_dst = id_dfd_dst
        self.id_dfd_link = id_dfd_link
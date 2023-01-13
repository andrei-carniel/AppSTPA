class Sec_Hierarchy(object):
    name = ""  # String
    name_trust_boundary = 0 # Integer
    source = ""  # String
    source_trust_boundary = 0  # Integer
    sources_list = []
    destiny = ""  # String
    destiny_trust_boundary = 0  # Integer
    action_name = ""  # String
    actions_list = []  # List
    attack_name = ""  # String
    attacks_list = []  # List
    control_name = ""  # String
    controls_list = []  # List
    is_link = False  # Boolean
    is_to_delete = False  # Boolean


    def __init__(self):
        self.name = "" # String
        self.name_trust_boundary = 0  # Integer
        self.source = "" # String
        self.source_trust_boundary = 0  # Integer
        self.sources_list = [] # List
        self.destiny = "" # String
        self.destiny_trust_boundary = 0  # Integer
        self.action_name = "" # String
        self.actions_list = [] # List
        self.attack_name = "" # List
        self.attacks_list = [] # List
        self.control_name = "" # String
        self.controls_list = [] # List
        self.is_link = False # Boolean
        self.is_to_delete = False # Boolean

    # def __init__(self, name, source, destiny, action_name, actions_list, attacks_list, controls_list, is_link):
    #     self.name = name # String
    #     self.source = source # String
    #     self.destiny = destiny # String
    #     self.action_name = action_name # String
    #     self.actions_list = actions_list # List
    #     self.attacks_list = attacks_list # List
    #     self.controls_list = controls_list # List
    #     self.is_link = is_link # Boolean
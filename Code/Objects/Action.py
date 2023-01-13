class Action:

    def __init__(self, id, source, destiny, name, name_ontology, name_link, name_component=""):
        self.id = id  # INTEGER PRIMARY KEY AUTOINCREMENT
        self.source = source  # INTEGER PRIMARY KEY AUTOINCREMENT
        self.destiny = destiny  # INTEGER PRIMARY KEY AUTOINCREMENT
        self.name = name  # TEXT NOT NULL
        self.name_ontology = name_ontology  # TEXT NOT NULL
        self.name_link = name_link  # TEXT NOT NULL
        self.name_component = name_component  # TEXT NOT NULL

class Action_Component:

    def __init__(self, id, id_component_src, name, begin_date, edited_date, id_project):
        self.id = id  # INTEGER PRIMARY KEY AUTOINCREMENT
        self.id_component_src = id_component_src  # INTEGER NOT NULL
        self.name = name  # TEXT NOT NULL
        self.begin_date = begin_date  # TEXT NOT NULL
        self.edited_date = edited_date  # TEXT
        self.id_project = id_project  # FK


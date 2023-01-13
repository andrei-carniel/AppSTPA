class Loss:

    def __init__(self, id, id_project, id_loss, description, begin_date, edited_date):
        self.id = id  # INTEGER PRIMARY KEY AUTOINCREMENT
        self.id_project = id_project  # INTEGER NOT NULL
        self.id_loss = id_loss  # INTEGER NOT NULL
        self.description = description  # TEXT NOT NULL
        self.begin_date = begin_date  # TEXT NOT NULL
        self.edited_date = edited_date  # TEXT


class Loss_Scenery:

    def __init__(self, side, onto_name, component, causes, requirement, id_controller, id_component, id_component_src, id_component_dst, name_src = "", name_dst = "", mechanism = ""):
        self.side = side
        self.onto_name = onto_name
        self.component = component
        self.causes = causes
        self.requirement = requirement
        self.id_controller = id_controller
        self.id_component = id_component
        self.id_component_src = id_component_src
        self.id_component_dst = id_component_dst
        self.name_src = name_src
        self.name_dst = name_dst
        self.mechanism = mechanism

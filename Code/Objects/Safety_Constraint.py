class Safety_Constraint:

    def __init__(self, id, id_project, id_safety_constraint, description, begin_date, edited_date, list_of_hazards=[]):
        self.id = id  # INTEGER PRIMARY KEY AUTOINCREMENT
        self.id_project = id_project  # INTEGER NOT NULL
        self.id_safety_constraint = id_safety_constraint  # INTEGER NOT NULL
        self.description = description  # TEXT NOT NULL
        self.begin_date = begin_date  # TEXT NOT NULL
        self.edited_date = edited_date  # TEXT
        self.list_of_hazards = list_of_hazards  # TEXT

class Safety_Constraint_Hazard:

    def __init__(self, id, id_project, id_constraint, id_hazard, id_haz_screen = 0):
        self.id = id  # INTEGER PRIMARY KEY AUTOINCREMENT
        self.id_project = id_project  # INTEGER NOT NULL
        self.id_hazard = id_hazard  # INTEGER NOT NULL
        self.id_constraint = id_constraint  # INTEGER NOT NULL
        self.id_haz_screen = id_haz_screen  # INTEGER NOT NULL
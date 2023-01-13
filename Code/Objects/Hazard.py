class Hazard:

    def __init__(self, id, id_project, id_hazard, description, begin_date, edited_date, identifier_loss=0, list_of_loss=[]):
        self.id = id  # INTEGER PRIMARY KEY AUTOINCREMENT
        self.id_project = id_project  # INTEGER NOT NULL
        self.id_hazard = id_hazard  # INTEGER NOT NULL
        self.description = description  # TEXT NOT NULL
        self.begin_date = begin_date  # TEXT NOT NULL
        self.edited_date = edited_date  # TEXT
        self.identifier_loss = identifier_loss # INTEGER
        self.list_of_loss = list_of_loss

class Hazard_Loss:

    def __init__(self, id, id_project, id_hazard, id_loss, id_loss_screen = 0):
        self.id = id  # INTEGER PRIMARY KEY AUTOINCREMENT
        self.id_project = id_project  # INTEGER NOT NULL
        self.id_hazard = id_hazard  # INTEGER NOT NULL
        self.id_loss = id_loss  # INTEGER NOT NULL
        self.id_loss_screen = id_loss_screen  # INTEGER NOT NULL
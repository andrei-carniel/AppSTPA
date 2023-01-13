class Variables:

    def __init__(self, id, id_component, id_project, name, begin_date, edited_date):
        self.id = id  # INTEGER PRIMARY KEY AUTOINCREMENT
        self.id_component = id_component  # INTEGER NOT NULL
        self.id_project = id_project  # INTEGER NOT NULL
        self.name = name  # TEXT NOT NULL
        self.begin_date = begin_date  # TEXT NOT NULL
        self.edited_date = edited_date  # TEXT


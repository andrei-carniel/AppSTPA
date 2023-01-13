class Assumptions:

    def __init__(self, id, id_project, id_assumption, description, begin_date, edited_date):
        self.id = id  # INTEGER PRIMARY KEY AUTOINCREMENT
        self.id_project = id_project  # INTEGER NOT NULL
        self.id_assumption = id_assumption  # INTEGER NOT NULL
        self.description = description  # TEXT NOT NULL
        self.begin_date = begin_date  # TEXT NOT NULL
        self.edited_date = edited_date  # TEXT


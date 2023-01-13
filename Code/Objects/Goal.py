class Goal:

    def __init__(self, id, id_project, id_goal, description, begin_date, edited_date):
        self.id = id  # INTEGER PRIMARY KEY AUTOINCREMENT
        self.id_project = id_project  # INTEGER NOT NULL
        self.id_goal = id_goal  # INTEGER NOT NULL
        self.description = description  # TEXT NOT NULL
        self.begin_date = begin_date  # TEXT NOT NULL
        self.edited_date = edited_date  # TEXT


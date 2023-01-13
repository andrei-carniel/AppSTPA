class Variable_Values:

    def __init__(self, id, id_variable, value, begin_date, edited_date):
        self.id = id  # INTEGER PRIMARY KEY AUTOINCREMENT
        self.id_variable = id_variable  # INTEGER NOT NULL
        self.value = value  # TEXT NOT NULL
        self.begin_date = begin_date  # TEXT NOT NULL
        self.edited_date = edited_date  # TEXT


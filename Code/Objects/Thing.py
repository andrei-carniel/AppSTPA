class Thing:

    def __init__(self, id, name, ontology_name):
        self.id = id  # INTEGER PRIMARY KEY AUTOINCREMENT
        self.name = name  # TEXT NOT NULL
        self.ontology_name = ontology_name  # TEXT NOT NULL


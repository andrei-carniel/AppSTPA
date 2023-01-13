class Loss_Scenario_Req:

    def __init__(self, id, id_controller, id_uca, id_project, id_comp_cause, id_comp_src, id_comp_dst, requirement, cause, mechanism = "",
                 name_src = "", name_dst = "", name_cause = "", performance_req = "", list_res = []):
        self.id = id
        self.id_controller = id_controller
        self.id_uca = id_uca
        self.id_project = id_project
        self.id_comp_cause = id_comp_cause
        self.id_comp_src = id_comp_src
        self.id_comp_dst = id_comp_dst
        self.requirement = requirement
        self.cause = cause
        self.mechanism = mechanism
        self.name_src = name_src
        self.name_dst = name_dst
        self.name_cause = name_cause
        self.performance_req = performance_req
        self.list_res = list_res
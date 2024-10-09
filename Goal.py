class Goal:
    def __init__(self, raw_string,not_among_goals_at_start=False,created_in_iteration_number=-1):
        self.raw_string = raw_string
        self.goal_string = self.raw_string
        self.not_among_goals_at_start = not_among_goals_at_start
        self.created_in_iteration_number = created_in_iteration_number

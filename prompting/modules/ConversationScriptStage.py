class ConversationScriptStage:
    def __init__(self, name, goal, check_is_complete, pool=None, show_missing=False, show_complete=False):
        self.name = name
        self.goal = goal
        self.check_is_complete = check_is_complete
        self.is_complete = check_is_complete()
        self.pool = pool
        self.show_missing = show_missing
        self.show_complete = show_complete
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
class Property:
    def __init__(self, name, value, description, can_override=True, required=False, examples=[]):
        self.name = name
        self.value = value
        self.description = description
        self.can_override = can_override
        self.examples = examples
        self.required = required
    
    def __str__(self):
        return f"{self.name}: {self.value}"
    
    def __repr__(self):
        return f"{self.name}: {self.value}"

    def is_empty(self):
        if self.value == "" or self.value == None:
            return True
class PromptPath:
    def __init__(self, base_path, type="json"):
        self.base_path = base_path
        self.type = type
    
    def __call__(self, file):
        if(file == '.'):
            return self.base_path
        else:
            return self.base_path + file + "." + self.type

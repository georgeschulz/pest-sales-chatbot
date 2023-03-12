class LLMResult:
    def __init__(self, result, tokens):
        self.result = result
        self.tokens = tokens
    
    def __value__(self):
        return self.result
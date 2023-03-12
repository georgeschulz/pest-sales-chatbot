from LLMResult import LLMResult

class GenExtract:
    def __init__(self, generator, extractor):
        self.generator = generator
        self.extractor = extractor
        self.total_tokens = 0
        self.total_runs = 0
        self.average_tokens = self.get_average_tokens()
    
    def run(self, input):
        raw_text = self.generator.run(input)
        #check if raw text is a LLMResult
        completion = raw_text
        self.total_runs += 1
        if isinstance(raw_text, LLMResult):
            completion = raw_text.result
            self.total_tokens += raw_text.tokens
        return self.extractor(completion)
    
    def prompt(self):
        print(self.generator.prompt.template)
    
    def __call__(self, input):
        return self.run(input)
    
    def get_average_tokens(self):
        if self.total_runs == 0:
            return None
        return self.total_tokens / self.total_runs
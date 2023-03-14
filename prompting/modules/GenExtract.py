from LLMResult import LLMResult

class GenExtract:
    def __init__(self, generator, extractor, print_intermediate=False):
        self.generator = generator
        self.extractor = extractor
        self.total_tokens = 0
        self.total_runs = 0
        self.average_tokens = self.get_average_tokens()
        self.print_intermediate = print_intermediate
    
    def run(self, input):
        raw_text = self.generator.run(input)
        #check if raw text is a LLMResult
        completion = raw_text
        self.total_runs += 1
        if isinstance(raw_text, LLMResult):
            completion = raw_text.result
            self.total_tokens += raw_text.tokens
        extracted = self.extractor(completion)
        if self.print_intermediate:
            print('Generation: ', raw_text.result)
        return extracted
    
    def prompt(self):
        print(self.generator.prompt.template)
    
    def __call__(self, input):
        return self.run(input)
    
    def get_average_tokens(self):
        if self.total_runs == 0:
            return None
        return self.total_tokens / self.total_runs
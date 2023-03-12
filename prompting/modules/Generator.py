from langchain.callbacks import get_openai_callback
from langchain.llms import OpenAIChat
from langchain.prompts import load_prompt
from langchain import LLMChain
import os
from LLMResult import LLMResult

#generator is a class for loading a prompt and runnning it
class Generator:
    def __init__(self, path):
        self.path = path
        self.prompt = load_prompt(path)
        self.llm = OpenAIChat(openai_api_key=os.getenv('OPENAI_KEY'))
        self.llm_chain = LLMChain(prompt=self.prompt, llm=self.llm, output_key="text")
    
    def run(self, input):
        with get_openai_callback() as cb:
            result = self.llm_chain.run(input)
            tokens = cb.total_tokens
            result = LLMResult(result, tokens)
            return result
    
    def __call__(self, input):
        return self.run(input)
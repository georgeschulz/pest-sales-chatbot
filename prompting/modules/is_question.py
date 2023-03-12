from GenExtract import GenExtract
from Generator import Generator
from Extractor import Extractor

is_question = GenExtract(
    Generator('prompts/response_is_question/initial_short_language_clarified.json'), 
    Extractor(regex=r"(True|False)")    
)

from Generator import Generator
from Extractor import Extractor
from GenExtract import GenExtract

is_issue = GenExtract(
    Generator('prompts/response_is_customer_issue/base_prompt_detailed.json'), 
    Extractor(regex=r"(True|False)")
)


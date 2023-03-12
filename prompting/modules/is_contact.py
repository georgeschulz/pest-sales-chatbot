from GenExtract import GenExtract
from Generator import Generator
from Extractor import Extractor

is_contact = GenExtract(
    Generator('prompts/response_is_contact_info/short-precise-add-names.json'), 
    Extractor(regex=r"(True|False)")
)

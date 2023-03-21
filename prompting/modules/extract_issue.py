from Generator import Generator
from Extractor import Extractor
from GenExtract import GenExtract

extract_issue = GenExtract(
    Generator('prompts/customer_issues_extractor/map_summarize_location_size.json'),
    Extractor(type="natural_language_to_dict", keys=["pest_id", "special_instructions", "location", "square_footage"]),
    print_intermediate=True
)

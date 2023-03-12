from Generator import Generator
from Extractor import Extractor
from GenExtract import GenExtract

extract_contact = GenExtract(
    Generator('prompts/contact_extractor/base_prompt.json'), 
    Extractor(type="natural_language_to_dict", 
              keys=["first_name", 
                    "last_name", 
                    "phone_number", 
                    "email",
                    "street_address", 
                    "city",
                    "state", 
                    "zip"
                    ])
)
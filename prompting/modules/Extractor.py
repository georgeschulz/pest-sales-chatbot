import re

class Extractor:
    def __init__(self, type="regex", regex=None, default="No Classification Found", keys=None):
        self.type = type
        self.regex = regex
        self.default = default
        self.keys = keys
    
    def first_regex_extractor(self, input, regex, default="No Classification Found"):
        match = re.search(regex, input)
        return_value = default
        if match:
            return_value = match.group(0)
        return return_value
    
    def natural_language_to_dict_extractor(self, input):
        #Search for every instance of a line that has a characterisitc, then a colon, then a value (ex. "Name: John")
        regex = re.compile(r"(\w+): ([\w.,@ \t-]+)", re.DOTALL)
        matches = re.findall(regex, input)
        #Then, add the characteristic and value to a dictionary
        dictionary = {}
        for match in matches:
            key = match[0].strip().lower()
            if key in self.keys and not self.keys == None:
                value = match[1].strip()
                if value == "None" or value == "none":
                    value = None
                dictionary[key] = value
        #Then, return the dictionary
        return dictionary


    def __call__(self, raw_text):
        if self.type == "regex":
            return self.first_regex_extractor(raw_text, self.regex, self.default)
        elif self.type == "natural_language_to_dict":
            return self.natural_language_to_dict_extractor(raw_text)
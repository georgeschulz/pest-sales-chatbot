from Property import Property

class NaturalLanguagePool:
    def __init__(self, data, description="", create_new_properties=False):
        self.data = data
        self.description = description
        self.create_new_properties = create_new_properties
        self._initial_data = data
    
    def natural_language(self):
        pool = ""
        for item in self.data:
            if item.is_empty():
                pool += f"{item.name}: ?\n"
            else:
                pool += f"{item.name}: {item.value}\n"
        return pool
    
    def clear_data(self):
        self.data = self._initial_data
    
    def property_exists(self, name):
        for item in self.data:
            if item.name == name:
                return True
        return False
    
    def update(self, data):
        #create a property if the property doesn't exist
        for i, prop in enumerate(data):
            if not self.property_exists(prop) and self.create_new_properties:
                new = Property(prop, data[prop], description="", can_override=True)
                self.data.append(new)
            else:
                #find the value of can_override of the property in self.data
                for item in self.data:
                    if item.name == prop:
                        #if can_override is true, update the value
                        if item.can_override and data[prop] != None and data[prop] != "" and data[prop] != "None":
                            item.value = data[prop]
            
    def get_missing_properties_for_context(self, verbose=False, use_examples=False):
        joiner = "; "
        if not verbose and not use_examples:
            joiner = ", "
        context_addition = []
        for item in self.data:
            missing_string = ""
            if item.required and item.is_empty():
                missing_string += f"{item.name}"
                if verbose:
                    missing_string += ", "
                    missing_string += item.description
                if use_examples:
                    if len(item.examples) > 0:
                        examples = ", ".join(item.examples)
                        if verbose:
                            missing_string += ","
                        missing_string += f" (ex. {examples})"
                    else:
                        missing_string += " "
                context_addition.append(missing_string)
        if len(context_addition) == 0:
            return 'All information collected'
        return joiner.join(context_addition)
    
    def dict(self):
        return {item.name: item.value for item in self.data}
    
    def is_complete(self):
        for item in self.data:
            if item.required and item.is_empty():
                return False
        return True
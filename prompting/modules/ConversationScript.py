class ConversationScript:
    def __init__(self, dependencies):
        self.dependencies = dependencies
    
    def __str__(self):
        return str(self.dependencies)
    
    def __repr__(self):
        return str(self.dependencies)
    
    def complete_next_dependency(self):
        for dependency in self.dependencies:
            if not dependency.is_complete():
                dependency.is_complete = True
                return dependency
            
    def get_next_dependency(self):
        for dependency in self.dependencies:
            if not dependency.is_complete:
                #check if the dependency is complete
                dependency.is_complete = dependency.check_is_complete()
                if not dependency.is_complete:
                    natural_language = f'Current goal: {dependency.goal}'
                    if dependency.show_missing and dependency.pool:
                        natural_language += '\nWhat we are missing: '
                        natural_language += f'{dependency.pool.get_missing_properties_for_context(verbose=False, use_examples=False)}'
                    if dependency.show_complete and dependency.pool:
                        natural_language += '\nWhat we have so far:\n'
                        natural_language += f'{dependency.pool.natural_language()}'
                    return natural_language
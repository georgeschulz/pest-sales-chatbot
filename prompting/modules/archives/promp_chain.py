class Prompt_Chain:
    def __init__(self, experiment_name, initial_prompt):
        self.experiment_name = experiment_name
        self.prompt = initial_prompt
    
    def user_says(self, user_input):
        self.prompt.append({ "role": "user", "content": user_input })
        return self

    def assistant_says(self, assistant_output):
        self.prompt.append({ "role": "assistant", "content": assistant_output })

    def wrap_text(self, text):
        text_to_print = ""
        if(len(text) > 200):
            for i in range(0, len(text), 200):
                text_to_print += text[i:i+200]
                text_to_print += " \n"
        print(text_to_print)
    
    def ask(self, user_text):
        self.user_says(user_text)
        response = generate_prompt(self.prompt, self.experiment_name)
        self.wrap_text(response)
        self.assistant_says(response)
    
    def refresh(self, initial_prompt):
        self.prompt = initial_prompt

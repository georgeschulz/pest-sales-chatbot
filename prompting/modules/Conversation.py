from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

from is_question import is_question
from is_contact import is_contact
from is_issue import is_issue
from extract_contact import extract_contact
from extract_issue import extract_issue

#TO DO: Make classifiers run only based on current dependencies and in parralel to lower latency

class Conversation:
    def __init__(self, history, model, dependencies, customer_profile, issues, policies, log_prompt=False):
        self.history = history
        self.model = model
        self.customer_profile = customer_profile
        self.issues = issues
        self.policies = policies
        self.dependencies = dependencies
        self.log_prompt = log_prompt

    def respond(self, message):
        #reload the context
        self.history.clear_context()
        
        #load the human's response
        human_response = HumanMessage(content=message)

        #build the contact profile 
        self.get_contact(message)

        #build the issue profile
        self.get_issue(message)

        #use the dependencies to inject the appropriate context and goals
        next_goal = self.dependencies.get_next_dependency()
        self.history.append_context(next_goal)
        
        #log the human's response so we have chain to review
        self.history.respond(human_response)

        #check if's a question to see if we need to load the policies
        is_message_a_question = is_question(message)

        #if the classifier says, it's a question, query the policies and add them to the context to increase truthfullness 
        if is_message_a_question:
            self.history.append_context("""Use the following pieces of context to answer the users question. If you don't know the answer, just say that you don't know, don't try to make up an answer.\n""")
            relevant_policies = self.policies.similarity_search(message, 1)
            policies_string = ""
            for policy in relevant_policies:
                policies_string += policy.page_content + "\n"
            self.history.append_context(policies_string)
            history = self.history.get()
            if self.log_prompt:
                self.log_prompt_clean(history)
            machine_response = self.model(history)
        else:
            history = self.history.get()
            if self.log_prompt:
                self.log_prompt_clean(history)
            machine_response = self.model(history)
        self.history.respond(AIMessage(content=machine_response.content))
        print('------------------')
        print('Agent: ', machine_response.content)
        if self.history.use_sum:
            self.history.remember(human_response.content, machine_response.content)
        #return machine_response
    
    def get_contact(self, message):
        #check if it's a message
        is_message_a_contact = is_contact(message)
        if is_message_a_contact:
            #extract the contact
            contact = extract_contact(message)
            #add the contact to the customer profile
            self.customer_profile.update(contact)
    
    def get_issue(self, message):
        issue = extract_issue(message)
        self.issues.update(issue)

    def log_prompt_clean(self, history):
        for message in history:
            if isinstance(message, HumanMessage):
                print('*Human*: ', message.content)
            elif isinstance(message, AIMessage):
                print('*Agent*: ', message.content)
            else:
                print('*System*: ', message.content)
from langchain.memory import ConversationSummaryMemory
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

class DynamicChatHistory:
    def __init__(self, model, system_message="", initial_history=[], additional_context=""):
        self.history = initial_history
        self.system_message = system_message
        self.additional_context = additional_context
        self.memory = ConversationSummaryMemory(llm=model)
    
    def respond(self, message):
        self.history.append(message)
        return self.history
    
    def get(self):
        total_history = []
        system_prompt = self.system_message # this is the base prompt
        summary = self.memory.load_memory_variables({})['history']
        if summary != "":
            system_prompt += "\nConversation Summary So Far:" + summary + '\n'
        else:
            system_prompt += "\nConversation Summary So Far: None. Just Started\n"
        #add the necessary context to the system prompt (ie. Natural Language Pools or Retrieval Info)
        system_prompt += " " + self.additional_context
        system_message = SystemMessage(content=system_prompt)
        total_history.append(system_message)
        #get the last element in self.history and add it to total_history
        total_history.append(self.history[-1])
        #print('Prompt (history): ', total_history)
        return total_history
    
    def set_context(self, context):
        self.additional_context = context
    
    def append_context(self, context):
        self.additional_context += context
    
    def clear_context(self):
        self.additional_context = ""

    def remember(self, human_message, machine_message):
        self.memory.save_context({'input': human_message}, {'output': machine_message})
        messages = self.memory.chat_memory.messages
        previous_summary = self.memory.load_memory_variables({})['history']
        self.memory.predict_new_summary(messages, previous_summary)
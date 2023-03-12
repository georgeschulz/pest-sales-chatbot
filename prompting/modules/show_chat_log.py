from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

def show_chat_log(history):
    for response in history.history:
        #get the type of response
        if isinstance(response, HumanMessage):
            print("*User*: " + response.content)
        elif isinstance(response, SystemMessage):
            print("*Initialization Prompt*: " + response.content)
        else:
            print("*Agent*: " + response.content)
        print('------------------------------------')
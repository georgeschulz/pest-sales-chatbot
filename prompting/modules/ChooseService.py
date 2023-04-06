#langchain imports
from langchain.llms import OpenAIChat
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import TransformChain, SequentialChain
from langchain import PromptTemplate, LLMChain

import pandas as pd
import nest_asyncio
import asyncio
import stripe
import os
import json
import re

from dotenv import load_dotenv
load_dotenv()
key = os.getenv('OPENAI_API_KEY')

#colors for output prints
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"
BOLD = "\033[1m"


chat = OpenAIChat(openai_api_key=key)
gpt4 = OpenAIChat(openai_api_key=key, model_name="gpt-4")
embeddings = OpenAIEmbeddings(openai_api_key=key)

all_services_df = pd.read_csv('data/services_search - Sheet1.csv')
all_services = []
for index, row in all_services_df.iterrows():
    all_services.append(row.to_dict())

#classes to make it easier to sample from the services specific characteristics for embeddings/context window
class Programs:
    def __init__(self, services):
        self.services = services

    def get_service(self, name):
        for service in self.services:
            if service['Name'] == name:
                return service
        return None
    
class Program:
    def __init__(self, dict):
        self.dict = dict

#create a container for a companys program offerings
all_services_list = Programs(all_services)

# Retrieve situational awareness from the vector store
situational_experience = Chroma(persist_directory='data/situation-db', embedding_function=embeddings)

def get_situational_awareness(inputs: dict) -> dict:
    #print(GREEN + 'STEP: Getting situational experiences' + RESET)
    conversastion = inputs["conversation_history"]
    knowledge = situational_experience.similarity_search(conversastion, 5)
    knowledge = [message.page_content for message in knowledge]
    #print(RED + 'Situational experiences found: ', knowledge, RESET) 
    #print(GREEN + 'STEP: Analyzing situational experiences' + RESET)       
    return { "situational_experience": knowledge }

retrieve_situational_awareness = TransformChain(transform=get_situational_awareness, input_variables=["conversation_history"], output_variables=["situational_experience"])

# Create a link that collapses nuggets of business knowledge with the customer's situation
analyze_situation_template = """Your goal is to identify how severe this issue is. Think step by step about your answer and use the information you provided to make you answer. After your analysis, please rate the severity as Low, Medium or High.
Conversation so Far: 
{conversation_history}
Property Type: {property_type}
Below are some possible practical experiences from our technicians that may be useful. Some of it may not be relevant to your answer.
{situational_experience}
----
Your Analysis:
"""

analyyze_situation_prompt = PromptTemplate(template=analyze_situation_template, input_variables=["situational_experience", "property_type", "conversation_history"])

analyze_issue_chain = LLMChain(
    llm=chat, 
    prompt=analyyze_situation_prompt, 
    output_key="situation_analysis"
)

severity_grade_template = """Provide a rating for the severity of the issue. Please rate the severity as "Low", "Medium" or "High".
Issue Analysis: {situation_analysis}
Your Rating:"""

severity_grade_prompt = PromptTemplate(template=severity_grade_template, input_variables=["situation_analysis"])

severity_grade_chain = LLMChain(llm=gpt4, prompt=severity_grade_prompt, output_key="severity_grade_raw")

def get_severity_grade(inputs: dict) -> dict:
    #print(GREEN + 'STEP: Getting severity grade' + RESET)
    response = inputs["severity_grade_raw"]
    pattern = re.compile(r'(Low|Medium|High)', re.IGNORECASE)
    matches = pattern.findall(response)

    if matches:
        response = matches[-1]
        severity_grade = response.strip().lower()
        #print(RED + 'Severity grade found: ', severity_grade, RESET)
    else:
        severity_grade = None
        #print(RED + 'Severity grade not found', RESET)
   
    return { "severity_grade": severity_grade }

get_severity_grade_chain = TransformChain(transform=get_severity_grade, input_variables=["severity_grade_raw"], output_variables=["severity_grade"])

# Create a link that fetches relevant services based on the analysis of the situation
service_description_search = Chroma(persist_directory='data/services-db', embedding_function=embeddings)

def get_relevant_services(inputs: dict) -> dict:
    analysis = inputs["situation_analysis"]
    #print(GREEN + 'STEP: Getting relevant services' + RESET)
    service_search_results = service_description_search.similarity_search(analysis, 3)
    #extract the services as a dict from the search results (they are json stored in .page_content)
    service_search_results = [json.loads(result.page_content) for result in service_search_results]
    detailed_services = []
    for service in service_search_results:
        service_name = service['Name']
        detailed_service = all_services_list.get_service(service_name)
        detailed_services.append(Program(detailed_service))

    relevant_services_text = ""
    for service in detailed_services:
        relevant_services_text += service.dict['Name'] + ": "
        relevant_services_text += service.dict['Description'] + "\n"
        relevant_services_text += "Best for: " + service.dict['Best for'] + "\n"
        relevant_services_text += "Covers: " + service.dict['Covered Pests'] + "\n"
        relevant_services_text += "Protection: " + service.dict['Level of Protection'] + "\n"
        relevant_services_text += "Price: " + service.dict['Cost'] + "\n\n"
    
    #print(RED + 'STEP: Completed getting services: ', detailed_services, RESET)
    #print(GREEN + 'STEP: Begin parsing the formulas' + RESET)

    for service in detailed_services:
        recurring_formula = service.dict['Recurring Formula']
        recurring_formula = recurring_formula.replace("{square_footage}", str(inputs["square_footage"]))
        recurring_formula = recurring_formula.replace("{target}", str(inputs["target"]))
        recurring_formula = recurring_formula.replace("{severity}", str(inputs["severity_grade"]))
        recurring_formula = recurring_formula.replace("{acres}", str(inputs["acres"]))
        service.dict['Recurring Formula'] = recurring_formula

        initial_formula = service.dict['Initial Formula']
        initial_formula = initial_formula.replace("{square_footage}", str(inputs["square_footage"]))
        initial_formula = initial_formula.replace("{target}", str(inputs["target"]))
        initial_formula = initial_formula.replace("{severity}", str(inputs["severity_grade"]))
        initial_formula = initial_formula.replace("{acres}", str(inputs["acres"]))
        service.dict['Initial Formula'] = initial_formula
    
    #print(GREEN + 'STEP: Completed parsing the formulas' + RESET)

    return { "relevant_services_dict": detailed_services, "relevant_services_text": relevant_services_text }

get_relevant_services_chain = TransformChain(transform=get_relevant_services, input_variables=["situation_analysis"], output_variables=["relevant_services_dict", "relevant_services_text"])

# calculate the prices based on the service objects
calculator_template = """Solve this excel formula. Briefly show your thinking for each step. Then write the answer as:
Answer: *answer*
Example:
=if(1=2, 1, 2) + 1
Thinking: 1=2 is false so the answer is 2 + 1
Answer: 3
Formula:
{formula}
"""

#majority vote will take in a list of results and return the most common answer for each type and name (ex. item: {'name': 'Service 1', 'answer': '5', 'type': 'recurring', 'iter_num': 0})
def majority_vote(results):
    # Group by name and type
    grouped_results = {}
    for result in results:
        name = result['name']
        type = result['type']
        if name not in grouped_results:
            grouped_results[name] = {}
        if type not in grouped_results[name]:
            grouped_results[name][type] = []
        grouped_results[name][type].append(result)

    # Find the most common answer for each name and type, excluding None unless it's the only result
    majority_vote_results = []
    for name in grouped_results:
        for type in grouped_results[name]:
            answers = [result['answer'] for result in grouped_results[name][type]]
            
            # Exclude None values if there are other non-None values
            non_none_answers = [answer for answer in answers if answer is not None]
            if non_none_answers:
                answers = non_none_answers

            answer = max(set(answers), key=answers.count)
            majority_vote_results.append({'name': name, 'answer': answer, 'type': type})

    return majority_vote_results


async def async_calculate_price(name, chain, formula, type, iter=1, timeout=8):
    max_retries = 3
    retries = 0
    answer = None
    
    while retries < max_retries:
        try:
            resp = await asyncio.wait_for(chain.arun(formula=formula), timeout=timeout)
            #print(BOLD, resp, RESET)
            # parse the Answer: *answer* from the response using regex
            answer = re.search(r'Answer:\s*\$?(\d+(?:\.\d+)?)\s*[^\d\(\)]*', resp)
            
            #if there is a match, break the loop
            if answer is not None:
                answer = answer.group(1)
                break
        except asyncio.TimeoutError:
            #print(RED + f"STEP: Timeout reached for {formula} after {timeout} seconds (Retry {retries + 1})" + RESET)
            retries += 1
    
    #if answer is None:
        #print(RED + f"STEP: Failed to parse answer from response after {max_retries} retries" + RESET)
    
    return { "name": name, "answer": answer, "type": type, "iter_num": iter }

async def get_pricing(inputs: dict) -> dict:
    #print(GREEN + 'STEP: Generating recurring price' + RESET)
    services = inputs["relevant_services_dict"]
    tasks = []
    for service in services:
        name = service.dict['Name']
        recurring_formula = service.dict['Recurring Formula']
        intial_formula = service.dict['Initial Formula']
        calculator_prompt = PromptTemplate(
            template=calculator_template,
            input_variables=["formula"]
        )
        chain = LLMChain(llm=chat, prompt=calculator_prompt, output_key="recurring_logic")
        #majority vote
        for n in range(1, 3):
            recurring_task = asyncio.create_task(async_calculate_price(name, chain, recurring_formula, 'recurring', iter=n))
            initial_task = asyncio.create_task(async_calculate_price(name, chain, intial_formula, 'initial', iter=n))
            tasks.append(recurring_task)
            tasks.append(initial_task)

    #print(GREEN + 'All Tasks Added to Queue' + RESET)
    results = await asyncio.gather(*tasks)
    #print(GREEN, 'All Tasks Completed' + RESET)
    #print(GREEN, 'Holding majority vote' + RESET)
    results = majority_vote(results)
    #print(GREEN, 'Majority vote complete' + RESET)

    for service in services:
        name = service.dict['Name']
        for result in results:
            if name == result['name'] and result['type'] == 'recurring':
                service.dict['Recurring Price'] = result['answer']
            if name == result['name'] and result['type'] == 'initial':
                service.dict['Initial Price'] = result['answer']
    
    service_offers_formatted = ""
    for service in services:
        service_offers_formatted += service.dict['Outward Facing'] + '\n'
        service_offers_formatted += 'Initial Price: $' + service.dict['Initial Price'] + '\n'
        service_offers_formatted += 'Recurring Price: $' + service.dict['Recurring Price'] + '\n'
        service_offers_formatted += 'Description: ' + service.dict['Description'] + '\n'
        service_offers_formatted += 'Covered Pests: ' + service.dict['Covered Pests'] + '\n'
        service_offers_formatted += 'Best For: ' + service.dict['Best for'] + '\n'
        service_offers_formatted += 'Frequency: ' + service.dict['Frequency'] + '\n'
        service_offers_formatted += 'Level of Protection: ' + service.dict['Level of Protection'] + '\n'
        service_offers_formatted += 'Benefits: ' + service.dict['Benefits'] + '\n'
        service_offers_formatted += 'Payment Link: <pay:' + service.dict['Name'] + '>\n'
        service_offers_formatted += '\n'

    return { "complete_services": services, "service_offers_formatted": service_offers_formatted }

def add_prices(inputs):
    loop = asyncio.get_event_loop()
    nest_asyncio.apply(loop)
    response = loop.run_until_complete(get_pricing(inputs))
    return { "complete_services": response["complete_services"], "service_offers_formatted": response['service_offers_formatted'] }


calculate_prices_chain = TransformChain(
    transform=add_prices, 
    input_variables=["relevant_services_dict"], 
    output_variables=["complete_services", "service_offers_formatted"]
)

pitch_template = """You are an expert and friendly salesperson for a pest control company company. You have just finished collecting information from the customer. Provide a helpful and entertaining explaination of the best service you found for them based on the following service and issue. Use informal language. Focus on service benefits and avoid being overly technical. Be casual and pretend you are chatting with a friend. Avoid using several emojis. Be brief because this is a chatbot conversation. You should customize your presentation of the offer based on the specifics of the customer's situation. At the end include the payment link. When selecting a service, here are your priorties:
1. Avoid selling too much more than the customer needs 
2. Try to sell an ongoing plan whereever possible unless the customer says they don't want one
3. Try a more expensive plan first if you think the customer can afford it
Continue the conversation with the customer.
Your Analysis: {situation_analysis}
Conversation So Far: 
{conversation_history}
Services you can choose from: 
{service_offers_formatted}
Your pitch:
"""

parser_prompt = PromptTemplate(template=pitch_template, input_variables=["conversation_history", "service_offers_formatted", "situation_analysis"])
sales_pitch_chain = LLMChain(llm=chat, prompt=parser_prompt, output_key="pitch")

class Payments:
    def __init__(self, api_key):
        self.api_key = api_key
    
    def create_payment_link(self, service_id, initial):
        stripe.api_key = self.api_key
        unit_amount = int(initial * 100)
        #create the price for the service in the stripe dashboard
        price = stripe.Price.create(currency="usd", unit_amount=unit_amount, product=service_id)
        price_id = price.id
        #create the payment link
        link = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='https://example.com/success',
            cancel_url='https://example.com/cancel',
        )
        return link.url


pay = Payments(api_key=os.getenv('STRIPE_KEY'))

def add_payment_links(inputs):
    #print('STEP: Getting payment links from stripe')
    services = inputs["complete_services"]
    updated_services = []
    for service in services:
        service_id = service.dict['Service ID']
        initial = float(service.dict['Initial Price'])
        if initial == 0:
            initial = float(service.dict['Recurring Price'])
        link = pay.create_payment_link(service_id, initial)
        service.dict['Payment Link'] = link
        updated_services.append(service)
    
    #print('STEP: Payment links added to services')
    #print('STEP: Creating pitch')
    return { "complete_services_with_links": updated_services }

payment_links_chain = TransformChain(
    transform=add_payment_links,
    input_variables=["complete_services"],
    output_variables=["complete_services_with_links"]
)

#add the payment link to the pitch
def parse_pitch(inputs):
    #print(GREEN, 'STEP: Pitch complete' + RESET)
    #print(GREEN, 'Adding payment link to pitch' + RESET)
    pitch = inputs["pitch"]
    #find the string in the form of <pay:service_name>
    payment_link = re.search(r'<pay:(.*?)>', pitch)
    if payment_link:
        #print(GREEN, 'Found payment link' + RESET)
        program_name = payment_link.group(1).strip()
    else:
        #print(RED, 'No payment link found' + RESET)
        program_name = ''
    #find the service that matches the name
    services = inputs["complete_services_with_links"]
    payment_link = "http://error.com"
    for service in services:
        if service.dict['Name'] == program_name:
            payment_link = service.dict['Payment Link']
    
    #replace the string with the payment link
    pitch = re.sub(r'<pay:(.*?)>', payment_link, pitch)
    #print(GREEN, 'Payment link added' + RESET)
    return { "final pitch": pitch }

parse_pitch_chain = TransformChain(
    transform=parse_pitch,
    input_variables=["pitch", "complete_services"],
    output_variables=["final pitch"]
)

analyze_situation_sequential = SequentialChain(
    chains=[
        retrieve_situational_awareness,
        analyze_issue_chain,
        severity_grade_chain,
        get_severity_grade_chain,
        get_relevant_services_chain,
        calculate_prices_chain,
        payment_links_chain,
        sales_pitch_chain,
        parse_pitch_chain
    ],
    input_variables=["square_footage", "property_type", "acres", "target", "conversation_history"],
    output_variables=[
        "situational_experience", 
        "situation_analysis", 
        "relevant_services_dict",
        "complete_services",
        "service_offers_formatted",
        "pitch",
        "final pitch",
        "severity_grade",
        "severity_grade_raw"
    ],
    verbose=True
)
from Property import Property
from NaturalLanguagePool import NaturalLanguagePool

#create a profile object with data that is a list of properties
first_name = Property("first_name", None, "The first name of the messenger", required=True, examples=['John', 'Jane'])
last_name = Property("last_name", None, "The last name of the messenger", required=True, examples=['Smith', 'Doe'])
phone = Property("phone_number", None, "The phone number of the person", required=True,  examples=['571-431-9531', '3133010343'])
email = Property("email", None, "The email of the person", required=True, examples=['timmie@yahoo.com'])
street_address = Property("street_address", None, "The street address of the person", required=True, examples=['123 Elm Way'])
city = Property("city", None, "The city of the person", required=True, examples=['Gaithersburg', 'Alexandria'])
state = Property("state", None, "The state of the person", required=True, examples=['MD', 'VA'])
zip = Property("zip", None, "The zip code of the person", required=True, examples=['20878', '22303'])

customer_profile = NaturalLanguagePool([first_name, last_name, phone, email, street_address, city, state, zip], "A profile of the person who sent the message")

from iexfinance.stocks import Stock
from iexfinance.refdata import get_symbols
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config
import random
import re
import string


patterns = {}


# create a Trainer
trainer = Trainer(config.load("config_spacy.yml"))

# load the training data
training_data = load_data("stock_training.json")

# Create an interpreter by training the model
interpreter = trainer.train(training_data)


# Define the states
# AUTHED and CHOOSE_TIME are pending states 
INIT = 0
GREET = 1
INTRODUCTION=2
CHOOSE_COMPANY=3
CHOOSE_FUNCTION=4
END = 5

responses = {"greet":["Hello!","Hey!"], 
             "introduction":["Hi, {}","Very nice to know you, {}! I can tell you about stock market, such as pirce, volume and market cap!"],
             "goodbye":["Bye,{}","See you {}"]}






# Define the policy rules

policy_rules = {
    (INIT, "greet"): (GREET, random.choice(responses["greet"])+" Can I have your name? "),
    (GREET,"introduction"):(INTRODUCTION, responses["introduction"]),
 
    (INTRODUCTION,"inquire"):(CHOOSE_COMPANY,"Which company do you want to know about?"),

    (CHOOSE_COMPANY, "specify_company"): (CHOOSE_FUNCTION, "What information do you want to know from {0}?"),
    (CHOOSE_FUNCTION, "price"): (CHOOSE_FUNCTION, "Current Stock Price:{0} Anything else?"),
    (CHOOSE_FUNCTION, "volume"): (CHOOSE_FUNCTION, "The latest Volume:{0} Anything else?"),
    (CHOOSE_FUNCTION, "market cap"): (CHOOSE_FUNCTION, "The latest Market Cap:{0} Anything else?"),
    (CHOOSE_FUNCTION, "goodbye"): (END,responses["goodbye"])
}




# Define a function to find the intent of a message
def match_intent(message):
    matched_intent = None
    for intent, pattern in patterns.items():
        # Check if the pattern occurs in the message 
        if pattern.search:
            matched_intent = intent
    return matched_intent

# Use regex to find names
def find_name(message):
    name = None
    # Create a pattern for checking if the keywords occur
    name_keyword = re.compile("name|call")
    # Create a pattern for finding capitalized words
    name_pattern = re.compile("[A-Z]{1}[a-z]*")
    if name_keyword.search(message):
    #if re.match(name_keyword,message):
        # Get the matching words in the string
        name_words = name_pattern.findall(message)
        #print(name_words)
        if len(name_words) > 0:
            # Return the name if the keywords are present
            name = ' '.join(name_words)
    return name




def respond(message):
    name = find_name(message)
    if name is None:
        print(bot_template.format("Hi I'm a stock chat robot!"))
    else:
        print(bot_template.format(random.choice(responses['greet']).format(name)))




# Intrepret the message by returning a next_state and Specific Info
def interpret(message):

    data = interpreter.parse(message)
    intent = data['intent']['name']
    entities = data["entities"]

    matched_intent = match_intent(message)
    if matched_intent =="greet":
    	return "greet",None


    if intent == "company_search":
    	for item in entities:
    		company_name = item["value"]
    		company_stock = Stock(company_name,token = api_token)
    		stock_batch = company_stock.get_quote()
    		return "specify_company", stock_batch['symbol']

    elif intent =="explanation":
    	return "introduction", None

    elif intent =="stock_search":
    	return "inquire", None

    elif intent == "information_search":
    	for item in entities:
    		if str(item["value"]) == "price":
    			return "price",stock_batch['latestPrice']
    		elif str(item["value"]) == "volume":
    			return "volume", stock_batch['latestVolume']
    		elif str(item["value"]) == "market cap":
    			return "market cap",stock_batch['marketCap']
    elif intent == "goodbye":
    	return "goodbye",None


# Sends a message to the bot
def send_message(state, message):
    print("USER : {}".format(message))
    new_state, info = interpret(message)
    print(info)
    if new_state == 'greet':
    	respond(message)
    	return state 

    next_state,response = policy_rules[(state,new_state)]

    if info is None:
    	print("BOT : {}".format(response))
    else: 
    	print("BOT : {}".format(response.format(info)))

    return next_state



if __name__ == '__main__':
    state = INIT
    while (True):
        print("USER : ", end = '')
        message = input()
        state = send_message(state,message)





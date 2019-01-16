import json
import logging
import random
from chatbot.parser.text_parser import TextParser
from ontology.sparql import QueryManager
#  pip install ipython
logging.getLogger().setLevel(logging.DEBUG)


class DialogueManager:
    
    def __init__(self):
        self.template_sentences = self.read_templates()
        self.query = QueryManager();
        
    def read_templates(self):
            template_sentences = []
            with open('contents/da_templates.json') as f:
                template_sentences = json.load(f)
                if logging.getLogger().isEnabledFor(logging.DEBUG):
                    for d in template_sentences:
                        logging.debug(d)
            return template_sentences
        
    def get_respond_message(self, respond_msg_key):
        messages = self.template_sentences[respond_msg_key]
        n_msgs = len(messages)
        if isinstance(messages, list) and n_msgs > 1:
            rand_num = random.randint(0, n_msgs - 1)
            return messages[rand_num]
        else:
            return messages[0]
        
    def get_respond_message_with_params(self, respond_msg_key, params):
        messages = self.template_sentences[respond_msg_key]
        n_msgs = len(messages)
        msg = ""
        if isinstance(messages, list) and n_msgs > 1:
            rand_num = random.randint(0, n_msgs - 1)
            msg = messages[rand_num]
        else:
            msg = messages[0]
        
        for index, value in params.items():
            msg = msg.replace("{" + str(index) + "}", value)
        
        return msg
    
    def execute_intent(self, req_da):
        logging.debug("executing...", req_da)
        intent_key = req_da["intent"]
        req_slots = req_da["slots"]
        if intent_key == "req_recommend_by_genre":
            return self.query.get_books_by_genre(req_slots)

        elif intent_key == "req_recommend_by_author":
            return self.query.get_books_by_author(req_slots)
        
        elif intent_key == "req_find_book_by_title": 
            # change function later  
            return self.query.query_by_book_title(req_slots)
        

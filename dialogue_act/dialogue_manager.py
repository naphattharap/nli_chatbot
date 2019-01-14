import json
import logging
import random
from chatbot.parser.text_parser import TextParser

#  pip install ipython
logging.getLogger().setLevel(logging.DEBUG)


class DialogueManager:

    def __init__(self):
        self.template_sentences = self.read_templates()
        
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
        if isinstance(messages, list) :
            num_msg = len(messages)
            rand_num = random.randint(0, num_msg - 1)
            return messages[rand_num]
        else:
            return messages
            

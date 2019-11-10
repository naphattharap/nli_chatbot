#!/usr/bin/env python
__author__ = "Naphatthara P."
__version__ = "1.0.0"
__email__ = "naphatthara.p@gmail.com"
__status__ = "Prototype"

import json
import logging
import random
import config
from ontology.sparql import QueryManager
#  pip install ipython
logging.getLogger().setLevel(logging.DEBUG)


class DialogueManager:
    
    def __init__(self):
        self.template_sentences = self.read_templates()
        self.query = QueryManager();
        
    def read_templates(self):
            # template_sentences = []
            # 'contents/da_templates.json'
            with open(config.DIALOGUE_TEMPLATE_PATH) as f:
                template_sentences = json.load(f)
                if logging.getLogger().isEnabledFor(logging.DEBUG):
                    for d in template_sentences:
                        logging.debug(d)
            return template_sentences
        
    def get_respond_message(self, respond_msg_key):
        messages = self.template_sentences[respond_msg_key]
        return random.choice(messages)
    
    def get_respond_recommend_books_by_author(self, respond_msg_key, author, books):
        """
        param is array of dictionary object {title, authors, genre, description, price}
        """
        book_titles = []
        for book in books:
            book_titles.append(book["title"])

        str_books = ",".join(book_titles)
        
        messages = self.template_sentences[respond_msg_key]
        template = random.choice(messages)
        resp_msg = template.format(author, str_books)

        return resp_msg
    
    def get_respond_recommend_books_by_genre(self, respond_msg_key, genre, books):
        """
        param is array of dictionary object {title, authors, genre, description, price}
        """
        book_titles = []
        for book in books:
            book_titles.append(book["title"])

        str_books = ",".join(book_titles)
        
        messages = self.template_sentences[respond_msg_key]
        template = random.choice(messages)
        resp_msg = template.format(genre, str_books)

        return resp_msg
    
    def get_respond_find_books_by_author(self, respond_msg_key, author, books):
        """
        param is array of dictionary object {title, authors, genre, description, price}
        """
        book_titles = []
        for book in books:
            book_titles.append(book["title"])

        str_books = ",".join(book_titles)
        
        messages = self.template_sentences[respond_msg_key]
        template = random.choice(messages)
        resp_msg = template.format(author, str_books)

        return resp_msg
    
    def get_respond_find_books(self, respond_msg_key, books):
        """
        param is array of dictionary object {title, authors, genre, description, price}
        """
#         book_titles = []
#         for book in books:
#             book_titles.append(book["title"])
# 
#         str_books = ",".join(book_titles)
        book = {}
        if len(books) == 0:
            return ""
        if len(books) > 0:
            book = books[0]

        messages = self.template_sentences[respond_msg_key + "_" + book["source"]]
        template = random.choice(messages)
        if template != "":
            resp_msg = template.replace("{authors}", book["authors"]).replace("{title}", book["title"]).replace("{genre}", book["genre"])
            if book["description"] != "":
                resp_msg = resp_msg.replace("{description}", book["description"])
            else:
                resp_msg = resp_msg.replace("{description}", "no information")
            
            if book["price"] != "":
                resp_msg = resp_msg.replace("{price}", book["price"])
            else:
                resp_msg = resp_msg.replace("{price}", "no information")
        
        else:
            resp_msg = "sorry I don't understand this."
        return resp_msg

    def get_respond_find_book_details(self, respond_msg_key, books):
        """
        param is array of dictionary object {title, authors, genre, description, price}
        """
#         book_titles = []
#         for book in books:
#             book_titles.append(book["title"])
# 
#         str_books = ",".join(book_titles)
        book = {}
        if len(books) == 0:
            return ""
        if len(books) > 0:
            book = books[0]

        messages = self.template_sentences[respond_msg_key + "_" + book["source"]]
        template = random.choice(messages)
        if template != "":
            resp_msg = template.replace("{authors}", book["authors"]).replace("{title}", book["title"]).replace("{genre}", book["genre"])
            if book["description"] != "":
                resp_msg = resp_msg.replace("{description}", book["description"])
            else:
                resp_msg = resp_msg.replace("{description}", "no information")
            
            if book["price"] != "":
                resp_msg = resp_msg.replace("{price}", book["price"])
            else:
                resp_msg = resp_msg.replace("{price}", "no information")
        
        else:
            resp_msg = "sorry I don't understand this."
        return resp_msg
  
    def execute_intent(self, req_da):
        logging.debug("executing...%s", req_da)
        intent_key = req_da["intent"]
        slots = req_da["slots"]
        
        default_res_key = "response_" + intent_key
        rec_max_results = 5
        find_max_results = 1
        if intent_key == "recommend_book_by_genre_intent":
            genre = slots["genre"]
            dict_results = self.query.recommend_book_by_genre_intent(genre, rec_max_results)
            return self.get_respond_recommend_books_by_genre(default_res_key, genre, dict_results)

        elif intent_key == "recommend_book_by_author_intent":
            author = slots["authors"]
            dict_results = self.query.recommend_book_by_author_intent(author, rec_max_results)
            return self.get_respond_recommend_books_by_author(default_res_key, author, dict_results)
        
        elif intent_key == "find_book_by_author_intent": 
            # change function later  
            authors = slots["authors"]
            dict_results = self.query.find_book_by_author_intent(authors, find_max_results)
            return self.get_respond_find_books(default_res_key, dict_results)
        
        elif intent_key == "find_book_by_title_intent": 
            # change function later  
            title = slots["title"]
            dict_results = self.query.find_book_by_title_intent(title, find_max_results)
            return self.get_respond_find_books(default_res_key, dict_results)
    
    def execute_action(self, req_params):
        logging.debug("executing...%s", req_params)
        
        action_func = req_params["next_action_func"]
        slots = req_params["slots"]
        
        default_res_key = "response_" + action_func
        if action_func == "find_book_details":
            dict_results = self.query.find_book_details(slots, max_result=1)
            return self.get_respond_find_book_details(default_res_key, dict_results)


# required lib name: rdflib 4.2.2
import logging

import rdflib
from rdflib.graph import ConjunctiveGraph, Namespace
import spacy
from textacy import spacy_utils
from ext_client.google_client import GoogleBookApiService
logging.getLogger().setLevel(logging.DEBUG)


class QueryManager:
    
    def __init__(self):
        # ontology and instances information are in this file
        self.g = rdflib.Graph()
        self.book_ontology = self.g.parse("ontology/book")
        self.g.serialize(format="n3")
        self.book_ontology_prefix = "PREFIX nli: <http://www.semanticweb.org/ont/nli#>"
        
    def query(self, query_statement):
        return list(self.g.query(query_statement))
    
    def print_query_result(self, query_statement):
        q_result = self.query(query_statement)
        for obj in q_result:
            print(obj.labels)   
            for e in obj:
                print(e)
    
    def get_books_by_genre(self, req_params):
        """
        Query ontology to find google API then call the API to get result
        """
        # TODO assume that got API from ontology
        # https://www.googleapis.com/books/v1/volumes?q=title:Harry%20Potter
        # https://www.googleapis.com/books/v1/volumes?q=subject:Art
        genre = req_params["genre"]

        googleBook = GoogleBookApiService()
        result = googleBook.search_by_genre(genre)
        return result
        
        # query
        
        # call API
        
        # generate response message and return
    
    def get_books_by_author(self, req_params):
        logging.info("param: %s", req_params)
        pass

    def find_book_by_title(self, req_params):
        logging.info("param: %s", req_params)
        pass
        
    def analyze_spo(self, g):
        for subj, pred, obj in g:
            print("s, p, o --> ", subj, pred, obj)
            if (subj, pred, obj) not in g:
                raise Exception("It better be!")

    def test_query1(self):
        # Query all 
        select_book_author = self.book_ontology_prefix + """
                        SELECT ?title ?name ?lastname WHERE {  
                             ?book nli:hasAuthor ?who .
                             ?who nli:firstName ?name . 
                             ?who nli:lastName ?lastname .
                             ?book nli:title ?title 
                         }"""
                         
        self.print_query_result(select_book_author)

    def query_by_book_title(self, book_title):
        # Query by Book title
        query_statement = self.book_ontology_prefix + """
                        SELECT ?title ?name ?lastname WHERE {  
                             ?book nli:hasAuthor ?who .
                             ?who nli:firstName ?name . 
                             ?who nli:lastName ?lastname .
                             ?book nli:title ?title .
                        FILTER regex(?title,\"""" + book_title + """\","i")
                         }"""
        self.query(query_statement)
        self.print_query_result(query_statement)

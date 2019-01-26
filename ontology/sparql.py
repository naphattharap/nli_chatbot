# required lib name: rdflib 4.2.2
import logging

from rdflib.graph import Graph, ConjunctiveGraph, Namespace

from ext_client.google_client import GoogleBookApiService

logging.getLogger().setLevel(logging.DEBUG)


class QueryManager:
    
    def __init__(self):
        # ontology and instances information are in this file
        self.g = Graph()
        # self.book_ontology = self.g.parse("ontology/book")
        self.g.parse("ontology.owl")
        # self.g.serialize(format="n3")
        self.book_ontology_prefix = "PREFIX nli: <http://www.semanticweb.org/jessie/ontologies/2018/10/Books#>"
        
    def query(self, query_statement):
        return list(self.g.query(query_statement))
    
    def query_result(self, query_statement):
        logging.debug("query %s", query_statement)
        q_result = self.query(query_statement)
        results = []
        for obj in q_result:
            for e in obj:
                results.append(e.__str__())
        return results;
    
    def get_books_by_genre(self, req_params):
        """
        Query ontology to find google API then call the API to get result
        """
        # TODO assume that got API from ontology
        # https://www.googleapis.com/books/v1/volumes?q=title:Harry%20Potter
        # https://www.googleapis.com/books/v1/volumes?q=subject:Art
        genre = req_params["genre"]
        googleBook = GoogleBookApiService()
        # result = googleBook.search_by_genre(genre)
        # return result
        
    def analyze_spo(self, g):
        for subj, pred, obj in g:
            print("s, p, o --> ", subj, pred, obj)
            if (subj, pred, obj) not in g:
                raise Exception("It better be!")

    def find_book_by_title(self, book_title):
        # Query by Book title
        query_statement = self.book_ontology_prefix + """
                        SELECT ?title ?author WHERE {  
                             ?book nli:hasAuthor ?who .
                             ?who nli:name ?author .
                             ?book nli:title ?title .
                        FILTER regex(?title,\"""" + book_title + """\","i")
                         }"""

        results = self.query_result(query_statement)
        print(results)
        return results
        
    def find_book_by_author(self, author):
        # Query by Book title
        query_statement = self.book_ontology_prefix + """
                         SELECT ?title ?genre WHERE {  
                               ?book nli:hasAuthor ?author .
                               ?book nli:title ?title .
                               ?book nli:genre ?genre .
                        FILTER regex(?author,\"""" + author + """\","i")
                         }"""
        # self.query(query_statement)
        # print(self.g.query(query_statement))
        # list_result = list(self.g.query(query_statement))
        # print(list_result[0][0])
        results = self.query_result(query_statement)
        print(results)
        return results


q = QueryManager()        
q.find_book_by_author("marie")
q.find_book_by_title("What Animal Thinks")

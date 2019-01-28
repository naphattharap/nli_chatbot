import logging

from rdflib.graph import Graph
from ext_client.google_client import GoogleBookApiService

logging.getLogger().setLevel(logging.DEBUG)

'''
SPARQL for querying data from ontology file
'''


class QueryManager:
    '''
    Query manager constructs SPARQL for each intent
    '''

    def __init__(self):
        # ontology and instances information are in this file
        self.g = Graph()
        self.g.parse("ontology/ontology.owl")
        # self.g.serialize(format="n3")
        self.book_ontology_prefix = " PREFIX nli: <http://www.semanticweb.org/jessie/ontologies/2018/10/Books#> "
        self.goole_api = GoogleBookApiService()

    def query_result(self, query_statement):
        """
        Query input statement
        """
        logging.debug("query %s", query_statement)
        q_result = list(self.g.query(query_statement))
        return q_result

    def convert_ontology_result_array(self, ontology_result):
        book_list = []
        # title, authors, description, genre, price

        for obj in ontology_result:
            book = {}
            book["title"] = obj[0].__str__()
            book["authors"] = obj[1].__str__()
            book["description"] = ""
            book["genre"] = obj[2].__str__()
            book["price"] = ""
            # add book to list
            book_list.append(book)
          
        return book_list 
   
    def convert_ontology_result(self, ontology_result):
        book_list = []
        # title, authors, description, genre, price
        
        if ontology_result != None and 'results' in ontology_result:
            results = ontology_result["results"]
            bindings = results["bindings"]
            for res_book in bindings:
                book = {}
                if 'title' in res_book:
                    book["title"] = res_book["title"]["value"]
                else: 
                    book["title"] = ""
                
                if 'name' in res_book:
                    book["authors"] = res_book["name"]["value"]
                else: 
                    book["authors"] = "" 
                    
                if 'description' in res_book:
                    book["description"] = res_book["description"]["value"]
                else: 
                    book["description"] = ""  
    
                if 'genre' in res_book:
                    book["genre"] = res_book["genre"]["value"]
                else: 
                    book["genre"] = "" 
                    
                if 'price' in res_book:
                    book["price"] = res_book["price"]["value"]
                else: 
                    book["price"] = "" 
                # add book to list
                book_list.append(book)
          
        return book_list  
        
    def recommend_book_by_genre_intent(self, genre, max_results):
        """
        Call to google API to search for books by genre.
        """      
        results = self.goole_api.google_book_by_author_intent(genre, max_results)
        
        logging.debug(results)
        return results
    
    def recommend_book_by_author_intent(self, author, max_results):
        """
        Call to google API to search for books by author name.
        """
        results = self.goole_api.google_book_by_author_intent(author, max_results)
        logging.debug(results)
        return results
    
    def find_book_by_author_intent(self, author, max_result):
        # Query by Book title
        query_statement = self.book_ontology_prefix + """
                        SELECT ?title ?name ?genre WHERE {  
                                ?book nli:hasAuthor ?author .
                                ?author nli:name ?name .
                                ?book nli:title ?title .
                                ?book nli:genre ?genre .
                        FILTER regex(?name,\"""" + author + """\","i")
                         }"""

        q_results = self.query_result(query_statement)
        results = self.convert_ontology_result_array(q_results)
        # self.convert_res_ontology(ontology_result)
        if len(results) == 0:
            results = self.goole_api.google_book_by_author_intent(author, max_result)
        logging.debug(results) 
        return results

    def find_book_by_title_intent(self, book_title, max_result):
        """
        Parse book title to SPARQL then query from ontology and convert result to array.
        """
        query_statement = self.book_ontology_prefix + """
                        SELECT ?title ?name ?genre 
                        WHERE { ?book nli:hasAuthor ?who . 
                                ?who nli:name ?name . 
                                ?book nli:title ?title .  
                                ?book nli:genre ?genre .
                        FILTER regex(?title,\"""" + book_title + """\","i")
                         }"""
        
        q_results = self.query_result(query_statement)
        results = self.convert_ontology_result_array(q_results)
        if len(results) == 0:
            results = self.goole_api.google_book_by_title_intent(book_title, max_result)
        logging.debug(results) 
        return results

# q = QueryManager()       
# print()
# print("------------------------")
# q.recommend_book_by_genre_intent("Fiction",5)
# print()
# print("------------------------")
# q.recommend_book_by_author_intent("Rowling", 5)
# print()
# print("------------------------")
# q.find_book_by_author_intent("Yaser", 1)
# print()
# print("------------------------")
# q.find_book_by_title_intent("Clean", 1)


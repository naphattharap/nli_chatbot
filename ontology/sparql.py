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
        self.goole_api_service = GoogleBookApiService()

    def query_result(self, query_statement):
        """
        Query input statement
        """
        logging.debug("query %s", query_statement)
        q_result = list(self.g.query(query_statement))
        results = []
        for obj in q_result:
            for e in obj:
                results.append(e.__str__())
        logging.debug("query result %s", results)
        return results
    
    def recommend_book_by_genre_intent(self, genre):
        """
        Call to google API to search for books by genre.
        """      
        result = self.goole_api_service.recommend_book_by_genre_intent(genre)
        return result
    
    def recommend_book_by_author_intent(self, author):
        """
        Call to google API to search for books by author name.
        """
        result = self.goole_api_service.recommend_book_by_author_intent(author)
        return result

    def find_book_by_title(self, book_title):
        """
        Parse book title to SPARQL then query from ontology and convert result to array.
        """
        query_statement = self.book_ontology_prefix + """
                        SELECT ?name WHERE {  
                             ?book nli:hasAuthor ?who .
                             ?who nli:name ?name .
                             ?book nli:title ?title .
                        FILTER regex(?title,\"""" + book_title + """\","i")
                         }"""

        results = self.query_result(query_statement)
        return results
        
    def find_book_by_author(self, author):
        # Query by Book title
        query_statement = self.book_ontology_prefix + """
                        SELECT ?title ?genre ?name WHERE {  
                                ?book nli:hasAuthor ?author .
                                ?author nli:name ?name .
                                ?book nli:title ?title .
                                ?book nli:genre ?genre .
                        FILTER regex(?name,\"""" + author + """\","i")
                         }"""

        results = self.query_result(query_statement)

        return results


q = QueryManager()        
q.find_book_by_author("haruki")
q.find_book_by_title("manual for cleaning")
# q.recommend_book_by_genre_intent("Fiction")
# q.recommend_book_by_author_intent("Rowling")


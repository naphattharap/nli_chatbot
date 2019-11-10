#!/usr/bin/env python
__author__ = "Naphatthara P."
__version__ = "1.0.0"
__email__ = "naphatthara.p@gmail.com"
__status__ = "Prototype"

from ontology.sparql import QueryManager

q = QueryManager(ontology_path='ontology.owl')       
print()
print("------------------------")
q.recommend_book_by_genre_intent("Fiction", 5)
print()
print("------------------------")
q.recommend_book_by_author_intent("Rowling", 5)
print()
print("------------------------")
q.find_book_by_author_intent("Yaser", 1)
print()
print("------------------------")
q.find_book_by_title_intent("Clean", 1)

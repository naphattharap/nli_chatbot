#required lib name: rdflib 4.2.2
import rdflib
from rdflib.graph import ConjunctiveGraph, Namespace

def print_query_resutl(list_result):
    for obj in list_result:
        print(obj)   
    
g = rdflib.Graph()

# ontology and instances information are in this file
result = g.parse("book")


# ?subject rdfs:subClassOf ?object
prefix = "PREFIX nli: <http://www.semanticweb.org/ont/nli#>"

select_book_author = prefix + """
                SELECT ?title ?name ?lastname WHERE {  
                     ?book nli:hasAuthor ?who .
                     ?who nli:firstName ?name . 
                     ?who nli:lastName ?lastname .
                     ?book nli:title ?title 
                 }"""
                 
book_author_result = list(g.query(select_book_author))
print_query_resutl(book_author_result)


# test triple
for triple in g:
    print("--triple--", triple)
    
l = list(g.query('select * where { ?s ?p ?o }'))
for s, p, o in l:
    print( "--s, p, o--", s, "----", p,  "----", o)

# Try query this one is not working yet
# l = list( g.triples((None,rdflib.URIRef('#writesBook'),None)) )
# for s, o in l:
#     print(s, "", o)
    



# Try filter data


# Try ASK



# Try DESCRIBE



for subj, pred, obj in g:
    print(subj, pred, obj)
    if (subj, pred, obj) not in g:
       raise Exception("It better be!")
s = g.serialize(format='n3')

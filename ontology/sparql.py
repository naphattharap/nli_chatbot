# required lib name: rdflib 4.2.2
import rdflib
from rdflib.graph import ConjunctiveGraph, Namespace
import spacy
from textacy import spacy_utils


def query(query_statement):
    return list(g.query(query_statement))


def print_query_result(query_statement):
    q_result = query(query_statement)
    for obj in q_result:
        print(obj.labels)   
        for e in obj:
            print(e)

    
g = rdflib.Graph()

# ontology and instances information are in this file
result = g.parse("book")
g.serialize(format="n3")

for subj, pred, obj in g:
    print("s, p, o --> ", subj, pred, obj)
    if (subj, pred, obj) not in g:
       raise Exception("It better be!")

s = g.serialize(format='n3')
print(s)

input_msg = "Who is author of Harry Potter"
nlp = spacy.load('en_core_web_sm')
doc = nlp(input_msg)
for sentence in doc.sents:
    root = sentence.root
    print("\nsentence:", sentence)
    print("\nroot:", root)
    print("\nsubject of root:", spacy_utils.get_subjects_of_verb(root))
    verbs = spacy_utils.get_main_verbs_of_sent(sentence)
    for v in verbs:
        print("\nsubject of root:", spacy_utils.get_span_for_verb_auxiliaries(v))
    print("\object:", spacy_utils.get_objects_of_verb(root))
#     print("\compound noun:", spacy_utils.get_span_for_compound_noun(noun))

# ?subject rdfs:subClassOf ?object
prefix = "PREFIX nli: <http://www.semanticweb.org/ont/nli#>"

# Query all 
select_book_author = prefix + """
                SELECT ?title ?name ?lastname WHERE {  
                     ?book nli:hasAuthor ?who .
                     ?who nli:firstName ?name . 
                     ?who nli:lastName ?lastname .
                     ?book nli:title ?title 
                 }"""
                 
print_query_result(select_book_author)

# Query by Book title
book_title = "Harry Potter"
select_book_author_by_title = prefix + """
                SELECT ?title ?name ?lastname WHERE {  
                     ?book nli:hasAuthor ?who .
                     ?who nli:firstName ?name . 
                     ?who nli:lastName ?lastname .
                     ?book nli:title ?title .
                FILTER regex(?title,\"""" + book_title + """\","i")
                 }"""

print_query_result(select_book_author_by_title)

# Try ASK
# SPARQL provides a simple ASK form that tests whether a pattern can be found in a graph. 
# The ASK keyword replaces the WHERE keyword, 
# and a simple boolean result is returned indicating whether there is a solution for the pattern in the graph. 

# author_firstname = "Yaser"
# desc_query  = prefix + """
#                 DESCRIBE  ?author
#                 WHERE {
#                    ?author nli:firstName "Yaser"^^xsd:string .
#                 }"""

# list_spo = query(desc_query)
# for s, p, o in list_spo:
#     print( "--s, p, o--", s, "----", p,  "----", o)

# test triple
for triple in g:
    print("--triple--", triple)
    for e in triple:
        print(e.label_info())
        print()
    
l = list(g.query('select * where { ?s ?p ?o }'))
for s, p, o in l:
    print("--s, p, o--", s, "----", p, "----", o)

# Try query this one is not working yet
# l = list( g.triples((None,rdflib.URIRef('#writesBook'),None)) )
# for s, o in l:
#     print(s, "", o)

# Try DESCRIBE


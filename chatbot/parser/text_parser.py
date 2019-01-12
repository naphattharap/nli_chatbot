# pip install spacy
# python -m spacy download en_core_web_sm
# conda install -c conda-forge spacy
# download exact model version (doesn't create shortcut link)
# PyCharm
# python -m spacy download en_core_web_sm-2.0.0 --direct
# python -m spacy download en_core_web_sm
# in case IDE is eClipse run below command at the interpreter
# -m spacy download en_core_web_sm-2.0.0 --direct 
import logging
import spacy
from IPython.display import display, Image
from spacy import displacy
import textacy.spacier.utils as spacy_utils


logging.getLogger("dialogue_manager").setLevel(logging.DEBUG)


class TextParser():
    # Load English tokenizer, tagger, parser, NER and word vectors

    def __init__(self):
        # load only once
        self.nlp = spacy.load('en_core_web_sm')
        

    def analyze_text(self, text):

        self.doc = self.nlp(text)
        self.print_doc()
        return self.doc

    def print_doc(self):
        # The Token class exposes a lot of word-level attributes.
        print("Token --> ")
        for token in self.doc:
            print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}".format(
                token.text,
                token.idx,
                token.lemma_,
                token.is_punct,
                token.is_space,
                token.shape_,
                token.pos_,
                token.tag_
            ))

        # Find named entities, phrases and concepts
        print("Text and Label --> ")
        for entity in self.doc.ents:
            print("text {} label {}".format(entity.text, entity.label_))

        print("doc.sent --> ")
        for sent in self.doc.sents:
            print(sent)

        # POS
        print("Part Of Speech --> ")
        print([(token.text, token.tag_) for token in self.doc])

        # NER (Name entity recognition)
        print("Name entity recognition --> ")
        for ent in self.doc.ents:
            print(ent.text, ent.label_)

        # Visualize name entity
        print("Visualize entity")
        displacy.render(self.doc, style='ent', jupyter=True)
        
      

        print("Dependency parsing --> ")
        for token in self.doc:
            print("{0}/{1} <--{2}-- {3}/{4}".format(
                token.text, token.tag_, token.dep_, token.head.text,
                token.head.tag_))

        print("Dependency tree --> ")
        displacy.render(self.doc, style='dep', jupyter=True,
                        options={'distance': 90})
        
        

    
    def get_dependency_parsing(self, text):
        self.doc = self.nlp(text);
        print("Dependency parsing --> ")
        for token in self.doc:
            print("{0}/{1} <--{2}-- {3}/{4}".format(
                token.text, token.tag_, token.dep_, token.head.text,
                token.head.tag_))
        
        for sentence in self.doc.sents:
            root = sentence.root
            subject = spacy_utils.get_subjects_of_verb(root)
            print("sentence", sentence, "\nroot", root, "\nsubject", subject)
            ask_about = spacy_utils.get_objects_of_verb(root)
            print("sentence", sentence, "\nroot", root, "\nobject of root", ask_about)
        
        
        verbs = spacy_utils.get_main_verbs_of_sent(self.doc)
        for v in verbs:
            obj = spacy_utils.get_objects_of_verb(v)
            print("\nverb", v, "\nobject", obj)
            
         
    def get_triple(self, sentence):
        pass
        
    
    def generate_response(self, sentence):
        # Extract entities
        doc = self.nlp(sentence)
        displacy.serve(doc, style='dep')
          
        for chunk in doc.noun_chunks:
            print(chunk.text, chunk.root.text, chunk.root.dep_,
                  chunk.root.head.text)
        
        for entity in doc.ents:
            print("entity {} label {}".format(entity.text, entity.label_))
        
        verbs = spacy_utils.get_main_verbs_of_sent(doc)
        print("main verbs: ", verbs)
        
        actions = {"hasAuthor": {"recommend, author, write"}}
        # title
        for sentence in doc.sents:
            root = sentence.root
            
            subject = spacy_utils.get_subjects_of_verb(root)
            print("sentence", sentence, "\nroot", root, "\nsubject", subject)
            ask_about = spacy_utils.get_objects_of_verb(root)
            print("sentence", sentence, "\nroot", root, "\nask about", ask_about)
        

        verbs = spacy_utils.get_main_verbs_of_sent(doc.sents)
        for v in verbs:
            obj = spacy_utils.get_objects_of_verb(v)
            print("\nverb", v, "\nobject", obj)
            
            
        # Extract entity's relationship


        for verb in verbs:
            print("\tverb: ", verb, "\tsubject:", spacy_utils.get_subjects_of_verb(verb),"\tobject: ", spacy_utils.get_objects_of_verb(verb))

        #doc = nlp(example_text)
        for sentence in doc.sents:
            print( "\tsubject of v_root: ",spacy_utils.get_subjects_of_verb(sentence.root),
                   "sentence root:", sentence.root, "\troot's lemma:",sentence.root.lemma_, 
                   "\tobject of v_root:", spacy_utils.get_objects_of_verb(sentence.root))
        
        
    
    def test(self):
        # Test
        # Process whole documents
        text = (u"Hello, do you have any recommended books?")
        
        parser = TextParser()
        parser.analyze_text(text)
        parser.get_n_triple(text)
        # Determine semantic similarities
        doc1 = parser.nlp(u"How are you doing?")
        doc2 = parser.nlp(u"Good Morning, how can I help you?")
        similarity = doc1.similarity(doc2)
        print("doc1 : ", doc1.text, "\ndoc2", doc2.text, "\nsimilarity",
              similarity)
        

        
    def test_triple(self, sentence):
        
        print(sentence)
        parser = TextParser()
        
        doc = self.nlp(sentence)
        verbs = spacy_utils.get_main_verbs_of_sent(doc)
        print("verbs: ", verbs)
        print(verbs)
        for verb in verbs:
            print("\tverb: ", verb, "\tsubject:", spacy_utils.get_subjects_of_verb(verb),"\tobject: ", spacy_utils.get_objects_of_verb(verb))

        #doc = nlp(example_text)
        for sentence in doc.sents:
            print( "\tsubject of v_root: ",spacy_utils.get_subjects_of_verb(sentence.root),
                   "sentence root:", sentence.root, "\troot's lemma:",sentence.root.lemma_, 
                   "\tobject of v_root:", spacy_utils.get_objects_of_verb(sentence.root))

    def para_to_ques(self, eg_text):
        doc = self.nlp(eg_text)
        results = []
        for sentence in doc.sents:
            root = sentence.root
            ask_about = spacy_utils.get_subjects_of_verb(root)
            answers = spacy_utils.get_objects_of_verb(root)
            
            if len(ask_about) > 0 and len(answers) > 0:
                if root.lemma_ == "be":
                    question = f'What {root} {ask_about[0]}?'
                else:
                    question = f'What does {ask_about[0]} {root.lemma_}?'
                results.append({'question':question, 'answers':answers})
        print(results)
        return results
    
#     
#a = TextParser()
#sentence = "Could you recommend the book written by Yaser Mostafa"
#a.generate_response("I am taking an NLI exam with Mareia")
# a.para_to_ques(sentence)
# sentence = "Hello, do you have books written by Mostafa?"
# # print("book is good though ".rfind('k'))
# # print("book".find('b'))
# a.test_triple(sentence)
# results = a.para_to_ques(sentence)
# print(results)
# 
# large_example_text = """
# Puliyogare is a South Indian dish made of rice and tamarind. 
# Priya writes poems. Shivangi bakes cakes. Sachin sings in the orchestra.
# 
# Osmosis is the movement of a solvent across a semipermeable membrane toward a higher concentration of solute. In biological systems, the solvent is typically water, but osmosis can occur in other liquids, supercritical liquids, and even gases.
# When a cell is submerged in water, the water molecules pass through the cell membrane from an area of low solute concentration to high solute concentration. For example, if the cell is submerged in saltwater, water molecules move out of the cell. If a cell is submerged in freshwater, water molecules move into the cell.
# 
# Raja-Yoga is divided into eight steps. The first is Yama. Yama is nonviolence, truthfulness, continence, and non-receiving of any gifts.
# After Yama, Raja-Yoga has Niyama. cleanliness, contentment, austerity, study, and self - surrender to God.
# The steps are Yama and Niyama. 
# """
# results = a.para_to_ques(large_example_text)
# print(results)
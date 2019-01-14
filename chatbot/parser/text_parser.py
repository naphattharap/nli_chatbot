# pip install spacy
# python -m spacy download en_core_web_sm
# conda install -c conda-forge spacy
# download exact model version (doesn't create shortcut link)
# PyCharm
# python -m spacy download en_core_web_sm-2.0.0 --direct
# python -m spacy download en_core_web_sm
# in case IDE is eClipse run below command at the interpreter
# -m spacy download en_core_web_sm-2.0.0 --direct 
import json
import logging
from pprint import pprint

from IPython.display import display, Image
from spacy import displacy
import spacy

import textacy.spacier.utils as spacy_utils

logging.getLogger("dialogue_manager").setLevel(logging.DEBUG)


class TextParser():
    # Load English tokenizer, tagger, parser, NER and word vectors

    def __init__(self):
        # load only once when parser is initialized.
        self.nlp = spacy.load('en_core_web_sm')
        self.intents = self.read_intent()
        
    def read_intent(self):
            intents_data = []
            with open('contents/intents.json') as f:
                intents_data = json.load(f)
                if logging.getLogger().isEnabledFor(logging.DEBUG):
                    for d in intents_data:
                        logging.debug(d)
            return intents_data

    def infer_intent(self, sentence):
        """
        Get main verbs and object then compare with existing intent 
        """   
        # Get main verbs and object
        # lemmarization of words here too.
        # parser = TextParser()
        doc = self.nlp(sentence)
        
        for sentence in doc.sents:
            root = sentence.root
            subject = spacy_utils.get_subjects_of_verb(root)
            print("sentence", sentence, "\nroot", root, "\nsubject", subject)
            ask_about = spacy_utils.get_objects_of_verb(root)
            print("sentence", sentence, "\nroot", root, "\nobject of root", ask_about)
        
        temp_input_match_words = []
        verbs = spacy_utils.get_main_verbs_of_sent(doc)
        for v in verbs:
            temp_input_match_words.append(v)
            obj = spacy_utils.get_objects_of_verb(v)
            if len(obj) > 0 : 
                temp_input_match_words.append(obj)
                print("\nverb", v, "\nobject", obj)
                
        input_match_words = temp_input_match_words.__str__()
#         print("input_match_words: ", input_match_words)
        
        # find similarity in intent with highest score.
        temp_score = 0
        target_intent = ""
        data = self.intents

        for intent in data:
            match_words = data[intent]["match_words"]
            doc_intent_match_words = self.nlp(match_words)
            doc_input_match_words = self.nlp(input_match_words)
            similarity_score = doc_input_match_words.similarity(doc_intent_match_words)
            print("input words : ", doc_input_match_words.text, "intent words: ", doc_intent_match_words.text, "\nsimilarity", similarity_score)
            if temp_score < similarity_score:
                target_intent = intent
                temp_score = similarity_score
                print("now intent is : ", target_intent)
        return self.intents[target_intent], temp_score

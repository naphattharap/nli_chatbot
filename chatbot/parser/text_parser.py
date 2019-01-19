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
        self.threshold_slot = 0.7;
        self.threshold_selected_choice = 0.8
        self.books_genre = ["cook", "comic", "children", "art", "history", "science"]
        self.books_title = ["Harry Potter"]
        self.books_author = ["Mostafa", "John", "Yaser"]
        
    def read_intent(self):
            intents_data = []
            with open('intents.json') as f:
            # with open('contents/intents.json') as f:
                intents_data = json.load(f)
                if logging.getLogger().isEnabledFor(logging.DEBUG):
                    for d in intents_data:
                        logging.debug(d)
            return intents_data
        
    def get_intent(self, intent_key):
        return self.intents[intent_key]

    def get_next_action(self, intent):
        return intent["next_action"]

    def get_fill_slots_action(self, action_key):
        return self.intents(action_key)
    
#     def extract_main_words(self, sentence):
#         """
#         Select only verb and object from sentence.
#         """
#         doc = self.nlp(sentence)
#         temp_input_match_words = []
#         verbs = spacy_utils.get_main_verbs_of_sent(doc)
#         for v in verbs:
#             temp_input_match_words.append(v)
#             obj = spacy_utils.get_objects_of_verb(v)
#             if len(obj) > 0 : 
#                 temp_input_match_words.append(obj)
#                 print("\nverb", v, "\nobject", obj)
#                 
#         return temp_input_match_words
    
    def process_entity_label(self, token):
        """
        Return entity label for Author, Book Title or Genre
        The result can be used as a slot key to fill in given token the slot
        """
        if token in self.books_genre:
            return "genre"
        
        if token in self.books_title:
            return "title"
        
        if token in self.books_author:
            return "author_name"
        return ""
    
    def process_auto_fill_slot(self, doc, slots):
        """
        Process doc for auto filling in given slots
        """
        for token in doc:
            if token.pos_ == "NOUN":
                target_slot_key = self.process_entity_label(token.text)
                if target_slot_key != "":
                    for slot_key, slot_value in slots.items():
                        if slot_value == "" and slot_key == target_slot_key:
                            slots[slot_key] = token.text

    def infer_intent(self, sentence):
        """
        Get main verbs and object then compare with existing intent 
        """   
        # Get main verbs and object
        # lemmarization of words here too.
        # parser = TextParser()
#         doc = self.nlp(sentence)
        
#         for sentence in doc.sents:
#             root = sentence.root
#             subject = spacy_utils.get_subjects_of_verb(root)
#             print("sentence", sentence, "\nroot", root, "\nsubject", subject)
#             ask_about = spacy_utils.get_objects_of_verb(root)
#             print("sentence", sentence, "\nroot", root, "\nobject of root", ask_about)
        doc = self.nlp(sentence)
        input_main_words = self.get_main_words(doc)
        
        entities = doc.ents
        for entity in entities:
            ent_label = self.process_entity_label(entity.text)
            if ent_label not in input_main_words:
                input_main_words.append(ent_label)
            
        input_match_words = ",".join(input_main_words)
        logging.debug("input keywords", input_match_words)
        # find similarity in intent with highest score.
        temp_score = 0
        target_intent = ""
        data = self.intents

        for intent in data:
            match_words = data[intent]["match_words"]
            if match_words == "": 
                # skip when the match word 
                continue
            
            doc_intent_match_words = self.nlp(match_words)
            doc_input_match_words = self.nlp(input_match_words)
            similarity_score = doc_input_match_words.similarity(doc_intent_match_words)
            print("input words : ", doc_input_match_words.text, "intent words: ", doc_intent_match_words.text, "\nsimilarity", similarity_score)
            if temp_score < similarity_score:
                target_intent = intent
                temp_score = similarity_score
        
        intent = self.intents[target_intent]
        if target_intent.startswith("req_"):
            # do auto filling in slot from sentence if applicable.
            slots = intent["slots"]
            self.process_auto_fill_slot(doc, slots)
        logging.debug("intent %s", target_intent) 
        return self.intents[target_intent], temp_score, target_intent
    
    def get_main_words(self, doc):
        words = []   
        target_pos = ["VERB", "NOUN"] 
        for token in doc:
            if token.pos_ in target_pos:
                words.append(token.lemma_)
            if token.pos_ == "NOUN":
                label = self.process_entity_label(token.text)
                if label != "" and label not in words:
                    words.append(label)
        return words
            
#         logging.debug("selected choice: ", selected_choice)        
#         doc = self.nlp(sentence)
#         nouns = self.get_nouns(doc)
#         logging.debug(nouns)
        
        for entity in doc.ents:
            logging.debug("text {} label {}".format(entity.text, entity.label_))
 
        for np in doc.noun_chunks:
            logging.debug(np.text)
    
    def infer_choice(self, sentence, choices):
        highest_similarity_score = 0;
        selected_choice = ""
        # main_words = self.extract_main_words(sentence)
            # search entity to fill in slot based on similarity of choice
        doc = self.nlp(sentence)
        main_words = self.get_main_words(doc)
        for token in main_words:
            for c in choices:
                score = self.nlp(token.lemma_).similarity(self.nlp(c))
                if(highest_similarity_score < score):
                    highest_similarity_score = score
                    selected_choice = c
        if highest_similarity_score >= self.threshold_selected_choice:
            return selected_choice
        else:
            # return empty because score is too low
            return "";
    
    def get_selected_choice(self, sentence, intent):
        """
        Finding slot in sentence.
        Check if input sentence matches with any in choices or not.
        If yes, return inferred slot otherwise return empty.
        """
        # split sentence into token
        doc = self.nlp(sentence)
        
        # compare if the word exist in slot choice or high similarity score of choice
        choices = intent["slots_choices"]
        len_choices = len(choices)
        highest_similarity_score = 0;
        selected_choice = ""
        main_words = self.extract_main_words(sentence)
        if len_choices > 0:
            # search entity to fill in slot based on similarity of choice
            for token in main_words:
                for c in choices:
                    score = self.nlp(token.lemma_).similarity(self.nlp(c))
                    if(highest_similarity_score < score):
                        highest_similarity_score = score
                        selected_choice = c
        if score >= self.threshold_selected_choice:
            return selected_choice
        else:
            # return empty because score is too low
            return "";

    def get_empty_slot(self, slots, filled_slots):
        n_slots = len(slots)
        if len(filled_slots) != n_slots:
            cnt = 0
            for slot in slots:
                slot_key = list(slots.value)[cnt]
                slot_val = slots[slot_key]
                cnt += 1
                if slot_val == "":
                    return slot_key

                
p = TextParser()
p.infer_intent("Do you have any recommend written by Yaser")

# p.find_slot_from_choices("I'm looking for a book about national language", "");

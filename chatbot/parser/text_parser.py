import json
import logging
import spacy

logging.getLogger("TextParser").setLevel(logging.DEBUG)


class TextParser():
    """
    Inferring the intent of speech.
    """

    def __init__(self):
        # load only once when parser is initialized.
        self.nlp = spacy.load('en_core_web_sm')
        self.intents = self.read_intent()
        self.threshold_intent = 0.7
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
        doc = self.nlp(sentence)
        input_main_words = self.get_main_words(doc)
        
        entities = doc.ents
        for entity in entities:
            ent_label = self.process_entity_label(entity.text)
            if ent_label not in input_main_words:
                input_main_words.append(ent_label)
            
        input_match_words = ",".join(input_main_words)
        logging.debug("input keywords %s", input_match_words)
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
            
            if temp_score < similarity_score:
                target_intent = intent
                temp_score = similarity_score
        
        if self.threshold_intent <= temp_score:
            intent = self.intents[target_intent]
        else:
            intent = ""
        
        logging.debug("intent %s", target_intent) 
        print("sentence: ", sentence, " \ntarget intent: ", target_intent, " \nsimilarity score: ", similarity_score)
        return target_intent
    
    def get_main_words(self, doc):
        words = []   
        target_pos = ["VERB", "NOUN", "ADJ"] 
        for token in doc:
            if token.pos_ in target_pos:
                words.append(token.lemma_)
            if token.pos_ == "NOUN":
                label = self.process_entity_label(token.text)
                if label != "" and label not in words:
                    words.append(label)
        return words
               
# p = TextParser()
# p.infer_intent("Any recommend book written by Yaser")
# p.infer_intent("I'm looking for a book about national language");

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
        self.books_genre = ["action and adventure", "alternate history", "anthology", "art",
                            "autobiography", "biography", "book review", "chick lit",
                            "children's literature", "classic", "comic book", "comics",
                            "coming-of-age", "cookbook", "crime", "detective", "diary",
                            "dictionary", "drama", "encyclopedia", "economics", "fable",
                            "fairytale", "fan fiction", "fantasy", "fiction", "folklore",
                            "graphic novel", "guide", "health", "historical fiction",
                            "history", "horror", "humor", "journal", "journalism", "legend",
                            "mathematics", "magical realism", "math", "memoir", "meta fiction",
                            "mystery", "mythology", "mythopoeia", "non fiction", "none fiction",
                            "non-fiction", "paranormal romance", "picture book", "poetry",
                            "political thriller", "prayer", "psychology", "realistic fiction", "reference book",
                            "religion, spirituality, and new age", "review", "romance", "satire",
                            "science fiction", "science", "self help book", "self help",
                            "short story", "shriller", "sociology", "suspense", "textbook", "psychological",
                            "travel", "true crime", "young adult", "learning language"]
        self.books_title = ["1q84", "a manual for cleaning women", "a room of one's own", "and still i rise",
                            "animal farm", "are we smart enough to know how smart animals are?",
                            "beyond words: what animals think and feel", "for whom the bell tolls",
                            "harry potter", "he lord of the rings", "inside of a dog", "la sombra del viento",
                            "learning from data", "life changing magic: a journal spark joy every day",
                            "pride and prejudice", "swing time", "the princess bride"]
        self.books_author = ["alexandra", "horowitz", "alexandra horowitz", "carl", "safina", "carl safina", "carlos ruiz zafón",
                             "ernest", "hemingway",
                             "frans de waal", "george", "orwell", "george orwell", "haruki", "murakami", "haruki murakami", "jane", "austen", "jane austen", "jk rowling",
                             "jrr tolkien", "lucia", "berlin", "marie kondo", "maya angelou", "virginia woolf",
                             "william goldman", "yaser", "mostafa", "yaser mostafa", "zadie smith"]
        
    def read_intent(self):
        intents_data = []
        with open('chatbot/parser/intents_with_slots.json') as f:
        # with open('chatbot/parser/intents.json') as f:
        # with open('intents.json') as f:
            intents_data = json.load(f)
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                for d in intents_data:
                    logging.debug(d)
        return intents_data

    def process_entity_label(self, token):
        """
        Return entity label for Author, Book Title or Genre
        The result can be used as a slot key to fill in given token the slot
        """
        lower_token = token.lower()
        
        if lower_token in self.books_genre:
            return "genre"
        
        if lower_token in self.books_title:
            return "title"
        
        if lower_token in self.books_author:
            return "authors"
        return ""

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
            
        input_match_words_str = ",".join(input_main_words)
        
        logging.debug("input keywords %s", input_match_words_str)
        # find similarity in intent with highest score.
        target_intent = ""
        data = self.intents
        
        print("from user: ", input_match_words_str)
        
        max_matched_word = 0
        for intent in data:
            match_words = data[intent]["match_words"]
            print("in intent: ", match_words)
            set_a = set(input_main_words)
            set_b = set(match_words.split(","))
            
            matched = set_a & set_b
            len_matched = len(matched)
            print("number of matched: ", len_matched)
            if match_words == "": 
                # skip when the match word 
                continue

            if max_matched_word < len_matched:
                target_intent = intent
                max_matched_word = len_matched
        
        if max_matched_word >= 2:
            intent = self.intents[target_intent]
             
        else:
            intent = ""
            target_intent = ""
        
        logging.debug("intent %s", target_intent) 
        # print("sentence: ", sentence, " \ntarget intent: ", target_intent, " \nsimilarity score: ", similarity_score)
        return self.intents[target_intent], target_intent
    
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

####################################################
# Scratch bot
####################################################

    def get_infer_intent(self, sentence):
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
            
        input_match_words_str = ",".join(input_main_words)
        
        logging.debug("input keywords %s", input_match_words_str)
        # find similarity in intent with highest score.
        target_intent = ""
        data = self.intents
        
        print("from user: ", input_match_words_str)
        
        max_matched_word = 0
        for intent in data:
            match_words = data[intent]["match_words"]
            print("in intent: ", match_words)
            set_a = set(input_main_words)
            set_b = set(match_words.split(","))
            
            matched = set_a & set_b
            len_matched = len(matched)
            print("number of matched: ", len_matched)
            if match_words == "": 
                # skip when the match word 
                continue

            if max_matched_word < len_matched:
                target_intent = intent
                max_matched_word = len_matched
        
        logging.debug("intent %s", target_intent) 
        if max_matched_word >= 2:
            intent = self.intents[target_intent]
            return self.intents[target_intent], target_intent, max_matched_word  
        else:
            return None, "", max_matched_word
    
    def get_intent(self, intent_key):
        return self.intents[intent_key] 
    
    def get_next_action(self, intent):
        return intent["next_action"]
 
    def get_fill_slots_action(self, action_key):
        return self.intents(action_key)
    
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
                
    def get_auto_fill_slots(self, sentence, arr_slots):
        """
        Check if user says the required slot.
        """
        filled_slots = {}   
        target_pos = ["NOUN", "ADJ"]
        doc = self.nlp(sentence)
        for token in doc:
            if token.pos_ in target_pos:
                label = self.process_entity_label(token.text)
                if label in arr_slots:
                    filled_slots[label] = token.text
        
        if len(filled_slots) == 0:
            entities = doc.ents
            for entity in entities:
                ent_label = self.process_entity_label(entity.text)
                if ent_label in arr_slots:
                    filled_slots[ent_label] = entity.text
                elif entity.label_ == "PERSON":
                    filled_slots["authors"] = entity.text
                
        return filled_slots      
                
    def get_matched_choice(self, sentence, choices):
        doc = self.nlp(sentence)
        main_words = self.get_main_words(doc)
        
        set_input = set(main_words)
        set_choice = set(choices.split(","))
        matched = set_input & set_choice
        
        if matched > 0:
            return matched
        else: 
            return ""

#     def get_entities(self, sentence):
#         for sent in nltk.sent_tokenize(sentence):
#             for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
#                 if hasattr(chunk, 'label'):
#                     print(chunk.label(), ' '.join(c[0] for c in chunk))

# t = TextParser()
# t.get_entities("tell me about The Lord of the Rings")

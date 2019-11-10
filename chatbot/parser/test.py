#!/usr/bin/env python
__author__ = "Naphatthara P."
__version__ = "1.0.0"
__email__ = "naphatthara.p@gmail.com"
__status__ = "Prototype"

from chatbot.parser.text_parser import TextParser

t = TextParser(intent_path='intents_with_slots.json')
sentence = "book by title animal farm"
intent_obj, target_intent, max_match_word = t.get_infer_intent(sentence)
print(target_intent)
slots = intent_obj["slots"]
t.get_auto_fill_slots(sentence, slots)

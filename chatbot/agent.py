#!/usr/bin/env python
__author__ = "Naphatthara P."
__version__ = "1.0.0"
__email__ = "naphatthara.p@gmail.com"
__status__ = "Prototype"

import logging
import gc

from chatbot.parser.text_parser import TextParser
from chatbot.stt.speech_recognizer import SpeechRecognizer
from chatbot.tts.speech_agent import SpeechAgent
import config
from dialogue.dialogue_act import DialogueAct
from dialogue.dialogue_manager import DialogueManager

logging.getLogger().setLevel(logging.DEBUG)


class ChatBotAgent:

    def __init__(self):
        """
        Initialize speech recoginer and text to speech agent
        """
        self.da = DialogueAct()
        self.d_manager = DialogueManager()
        self.parser = TextParser()
        self.listener, self.speaker = self.init_agents()
        self.req_params = {}  # keep request and slots 
        self.res_params = {}  
        self.session = {} 
        self.filled_slots = {}
        self.has_woken_up = False

    def init_agents(self):
        self.stt = SpeechRecognizer().init_recognizer(config.STT_GOOGLE, config.LANGUAGE_CODE)
        self.tts = SpeechAgent().init_agent(config.TTS_PYTTSX3)
        return self.stt, self.tts

    def ask_to_fill_slot(self, empty_slot_key):
        DA_ASK_PREFIX = "ask_for_"
        respond_message = self.d_manager.get_respond_message(DA_ASK_PREFIX + empty_slot_key)
        self.speaker.speak(respond_message)
    
    def reset_session(self):
        self.req_params = {}  # keep request and slots 
        self.res_params = {}  
        self.session = {} 
        self.filled_slots = {}
        self.has_woken_up = False
        gc.collect()
    
    def init_filled_slot_obj(self, arr_slot_key):
        for key in arr_slot_key:
            self.filled_slots[key] = ""
    
    def get_empty_slot_key(self):
        for key, value in self.filled_slots.items():
            if value == "":
                return key
        return ""

    def start(self):
        # Better to move below hardcode to configuration files
        wakeup_words = ["hi", "hello", "hey", "hey bot", "hey book bot", "hey bookbot", "bookbot"]
        end_converstion_words = ["bye", "bye bye", "goodbye", "see you"]
        greeting_msg = "Hello, how may I help you?"
        goodbye_msg = "Hope to see you again soon, bye."
        
        # Flag for greeting state
        greeting = False
        idle_state = True
        
        # service name
        current_intent = {}
        
        # each round conversation
        current_action = ""
        n_slots = 0
        current_idx_slot = 0
       
        target_intent = ""
        # constant to control key
        default_cannot_extract_intent_key = "default_unrecognize_intent"
        logging.debug("Now book bot is ready, please wake him up by saying hi to him")
        
        while True:
            try:
                if  greeting == False and idle_state == False:
                    self.speaker.speak(greeting_msg)
                    greeting = True
 
                # Listen voice from microphone and generate sentence.
                sentence = self.listener.listen()
                if sentence.startswith("Error"):
                    continue
                
                if sentence in wakeup_words:
                    response_msg = self.d_manager.get_respond_message("response_greeting")
                    self.speaker.speak(response_msg)
                    self.has_woken_up = True
                    idle_state = False
                    greeting = True
                    continue
                
                elif sentence in end_converstion_words:
                    response_msg = self.d_manager.get_respond_message("response_bye")
                    self.speaker.speak(response_msg)
                    self.has_woken_up = False
                    greeting = False
                    self.reset_session()
                    current_intent = {}
                    current_action = ""
                    n_slots = 0
                    current_idx_slot = 0
                    idle_state = True
                    continue

                da_result = self.da.predict(sentence)
                logging.debug("Predicted dialog type %s ", da_result)
                                # If type is end of conversation, stop program.
                
                if da_result == "Bye":  # and not is_flling_in_slot_action:
                    # TODO Jess  
                    response_msg = self.d_manager.get_respond_message("response_bye")
                    self.speaker.speak(response_msg)
                    self.reset_session()
                    continue
                
                elif da_result == "Greet":  # and not is_flling_in_slot_action:
                    response_msg = self.d_manager.get_respond_message("response_greeting")
                    self.speaker.speak(response_msg)
                    self.reset_session()
                    continue
                
                elif 'current_action' in self.session and self.session["current_action"] == "yn_answer":
                    if da_result == "yAnswer":
                        # Execute next action
                        req_params = {}
                        req_params["next_action_func"] = self.session["current_action_execute"]
                        req_params["slots"] = self.filled_slots
                        response_message = self.d_manager.execute_action(req_params)
                        self.speaker.speak(response_message)
                        self.reset_session()
                    elif da_result == "nAnswer" or da_result == "Reject":
                        # response to no.
                        response_msg = self.d_manager.get_respond_message("ynQuesion_reject")
                        self.speaker.speak(response_msg)
                        self.reset_session()
                else:
                    # Analyze entity in question find subject, predicate, object
                    # Query in ontology by SPARQL 

                    is_flling_in_slot_action = 'current_action' in self.session and self.session["current_action"] == "fill_slot"
                    if is_flling_in_slot_action:
                        # fill slot from sentence
                        self.filled_slots[self.session["current_filling_slot"]] = sentence
                        
                    # curent_intent = parser.infer_intent(sentence)
                    if not 'intent' in self.session:
                        intent_obj, target_intent, max_matched_word = self.parser.get_infer_intent(sentence)
                        if target_intent == "":
                            # can't recognize intent
                            response_message = self.d_manager.get_respond_message(default_cannot_extract_intent_key)
                            self.speaker.speak(response_message)
                            self.reset_session()
                            continue
                        elif target_intent != "" and target_intent.startswith("recommend_") and max_matched_word == 2:  # 2 is throshold in text_parser
                            # can't recognize exactly intent but user said some matched keyword
                            response_message = self.d_manager.get_respond_message("ask_for_choices_to_recommend")
                            self.session["current_action"] = "fill_slot"
                            # self.session["slots_choice"] = ["authors", "genre", "title"]
                            self.session["current_filling_slot"] = ""
                            self.speaker.speak(response_message)
                            # self.reset_session()
                            continue
                        else:
                            # Check auto fill in slot and take it from sentence if found
                            self.session["intent"] = target_intent
                            # Check there is slot to fill in.
                            slots = intent_obj["slots"]
                            self.init_filled_slot_obj(slots)
                            # Check number of slot to fill in.
                            n_slots = len(slots)
                            # Auto-filling in slot
                            auto_filled_slot = self.parser.get_auto_fill_slots(sentence, slots)
                            for key, value in auto_filled_slot.items():
                                if key in self.filled_slots:
                                    self.filled_slots[key] = value
                        
                    if target_intent.startswith("recommend") or target_intent.startswith("find"):                           
                        
                        empty_slot_key = self.get_empty_slot_key()
                        if  empty_slot_key != "":
                        # if n_slots < len(self.filled_slots):
                            self.session["current_action"] = "fill_slot"
                            # ask to fill slot
                            self.session["current_filling_slot"] = empty_slot_key
                            respond_message = self.d_manager.get_respond_message("ask_for_fill_slot_" + empty_slot_key)
                            self.speaker.speak(respond_message)
                            continue
                        else:
                            # all slot are filled.
                            # executes target request service
                            self.req_params["intent"] = target_intent
                            self.req_params["slots"] = self.filled_slots
                            # respond_msg_key = current_intent["respond_statement"]
                            response_message = self.d_manager.execute_intent(self.req_params)
                            self.speaker.speak(response_message)
                            if 'pre_next_action_msg' in intent_obj and intent_obj['pre_next_action_msg'] != "":
                                next_action_msg = intent_obj["pre_next_action_msg"]
                                respond_message = self.d_manager.get_respond_message(next_action_msg)
                                self.speaker.speak(respond_message)
                                # set next action after fill slot
                                self.session["current_action"] = "yn_answer"
                                self.session["current_action_execute"] = intent_obj["next_action_func"]
                            else:
                                self.reset_session()
                                
                            # 
                
                # When user said something and bot can't understand.
                if sentence != "" and target_intent == "":
                    respond_message = self.d_manager.get_respond_message(default_cannot_extract_intent_key)
                    self.speaker.speak(respond_message)
                    continue
                    # Problem, when there is no voice come, it returns error.
                    # So we handle by continue
                    # Continue next loop if Error is returned.

            except SystemExit:
                print("ignoring SystemExit")
            except Exception as e:
                print("Exception: " + e.__str__())
 

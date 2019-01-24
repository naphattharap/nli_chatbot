import logging

# from nltk.parse.featurechart import sent

from chatbot.parser.text_parser import TextParser
from chatbot.stt.speech_recognizer import SpeechRecognizer
from chatbot.tts.speech_agent import SpeechAgent
import config
from dialogue_act.dialogue_act import DialogueAct
from dialogue_act.dialogue_manager import DialogueManager

logging.getLogger().setLevel(logging.DEBUG)


# from dialogue_act.dialogue_manager import DialogueManager
# from dialogue_act.dialogue_mgt import DialogueActManager
class ChatBotAgent:

    def __init__(self):
        """
        Initialize speech recoginer and text to speech agent
        """
        self.da = DialogueAct()
        self.d_manager = DialogueManager()
        self.parser = TextParser()
        self.listener, self.speaker = self.init_agents()

    def init_agents(self):
        self.stt = SpeechRecognizer().init_recognizer(config.STT_GOOGLE)
        self.tts = SpeechAgent().init_agent(config.TTS_PYTTSX3)
        return self.stt, self.tts

    def ask_to_fill_slot(self, empty_slot_key):
        DA_ASK_PREFIX = "ask_for_"
        respond_message = self.d_manager.get_respond_message(DA_ASK_PREFIX + empty_slot_key)
        self.speaker.speak(respond_message)
        
    def start(self):
        # instance initialization
        # bot = ChatBotAgent()
        # dmngr = DialogueManager()

        wakeup_words = ["hi", "hello"]
        end_converstion_words = ["bye", "bye bye", "goodbye", "see you"]
        greeting = False
        greeting_msg = "Hello, how may I help you?"
        goodbye_msg = "Hope to see you soon, bye."
        
        req_params = {}  # keep request and slots 
        res_params = {}   
        # service name
        current_intent = ""
        
        # each round conversation
        current_action = ""
        filled_slots = []
        current_slot = ""
        n_slots = 0
        current_idx_slot = 0
        
        # constant to control key
        
        while True:
            try:
                if greeting == False:
                    greeting = True
                    self.speaker.speak(greeting_msg)

                # Listen voice from microphone and generate sentence.
                sentence = self.listener.listen()
                current_turn = "bot"  # user has already spoken
                if sentence == "Error":
                    continue
                # sentence = "Do you have any recommended books written by J k rowling"
                # sentence = "I would like to read books about psychology, do you have any recommendation"
                # sentence = "Do you have any recommended books in psychological category"
                # Check sentence with trained model for dialogue act.
                da_result = self.da.predict(sentence);
                print("DA type --> ", da_result)
                                # If type is end of conversation, stop program.
                if da_result == "Bye":
                    response_msg = self.da.respond("res_bye")
                    self.speaker.speak(response_msg)
                    # TODO!!!!!!!!!!! clear session here
                    continue
                
                elif da_result == "Greet":
                    response_msg = self.d_manager.get_respond_message("res_greeting")
                    self.speaker.speak(response_msg)
                    # TODO!!!!!!!!!!! clear session here
                    continue
                
                elif da_result == "whQuestion" or da_result == "ynQuestion" or da_result == "Statement" or da_result == "nAnswer":
                    # Analyze entity in question find subject, predicate, object
                    # Query in ontology by SPARQL 
                    # Generate sentence
                    # parser.get_dependency_parsing(sentence)
                    # parser.generate_response(sentence)
                    
                    # curent_intent = parser.infer_intent(sentence)
                    if current_action == "":
                        current_intent, similarity_score, target_intent = self.parser.infer_intent(sentence)
                        
                        respond_msg_key = current_intent["respond_statement"]
                        slots = current_intent["slots"]  # auto-filled slot from user sentence
                        filled_slots = slots  # keep all slots
                        n_slots = len(slots)
                        
                        if n_slots < len(filled_slots):
                            # just respond and finish this round
                            respond_message = self.d_manager.get_respond_message(respond_msg_key)
                            self.speaker.speak(respond_message)
    
                            # perform next action
                            current_action = current_intent["next_action"]
                            current_intent = self.parser.get_intent(current_action)
                            logging.debug("action: %s", current_action) 
                            continue
                        
                        elif target_intent.startswith("req_"):
        
                            # if it is request for service then check slot.
                            # check if there is slots to fill in
                            if n_slots != len(filled_slots):
                                # ask user to fill slot
                                empty_slot_key = self.parser.get_empty_slot(slots, filled_slots)
                                self.ask_to_fill_slot(empty_slot_key)
                                current_action = current_intent["fill_slots_action"]
                                
                                continue;
                            else:
                                # executes target request service
                                req_params["intent"] = target_intent
                                req_params["slots"] = filled_slots
                                respond_msg_key = current_intent["respond_statement"]
                                result = self.d_manager.execute_intent(req_params)
                                res_params[0] = result
                                respond_message = self.d_manager.get_respond_message_with_params(respond_msg_key, res_params)
                                self.speaker.speak(respond_message)
                                # pass result to respond message
                     
                     # Wait for user to fill in all slots.
                     
                    if current_action.startswith("fill_slots_"):
                        # if slots_choices is not empty, it means user has to select among choices
                        slots = current_intent["slots"]
                        n_slots = len(slots)
                        
                        if n_slots > 0:
                            # require to fill in slot
                            # keep what we are asking user to fill in.
                            current_slot_key = list(slots)[current_idx_slot]
                            current_slot_choice = slots[current_slot_key]
                            n_choices = len(current_slot_choice)
                            # check if slots come with choices and need to infer.
                            # n_choices = len(current_intent["slots_choices"])
                            if n_choices > 0:
                                selected_choice = self.parser.infer_choice(sentence, current_slot_choice)
                                if selected_choice == "":
                                    # what user said can't understand by bot
                                    default_unknow_choice = self.d_manager.get_respond_message("default_unknow_choice")
                                    self.speaker.speak(default_unknow_choice)
                                    self.speaker.speak(respond_message)
                                    continue
                                else:
                                    # filling in the slot by selected choice
                                    current_slot_value = selected_choice
                                    # req_service[current_slot_key] = current_slot_value
                                    filled_slots.append({current_slot_key : current_slot_value})
                                    # parser.fill_in_slots(sentence, current_intent, current_slot, selected_choice)
                                    
                                    # if all slots are filled in, execute next action
                                    if n_slots == len(filled_slots):
                                        next_action = self.parser.get_next_action(current_intent)
                                        if next_action.startwith("req_"):
                                            req_params["intent"] = next_action
                                            req_params["slots"] = filled_slots
                                            self.d_manager.execute_intent(req_params)
                                            logging.debug("take action %s", next_action)
                        else:
                            logging.debug("open answer, no choices")
                
                # Problem, when there is no voice come, it returns error.
                # So we handle by continue
                # Continue next loop if Error is returned.
                    
                # response_msg = da.respond(sentence)
                # Call dialogue management and speak
#               # reply_message = dmngr.process(sentence)
                # speaker.speak(response_msg)
                logging.debug(req_params)
            except SystemExit:
                print("ignoring SystemExit")
            except Exception as e:
                
                print("Exception: " + e.__str__())
 

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
        pass

    def init_agents(self):
        self.stt = SpeechRecognizer().init_recognizer(config.STT_GOOGLE)
        self.tts = SpeechAgent().init_agent(config.TTS_PYTTSX3)
        return self.stt, self.tts

    def start(self):
        # instance initialization
        # bot = ChatBotAgent()
        # dmngr = DialogueManager()
        da = DialogueAct()
        d_manager = DialogueManager()
        parser = TextParser()
        listener, speaker = self.init_agents()

        wakeup_words = ["hi", "hello"]
        end_converstion_words = ["bye", "bye bye", "goodbye", "see you"]
        greeting = False
        greeting_msg = "Hello, how may I help you?"
        goodbye_msg = "Hope to see you soon, bye."
        
        curent_intent = ""
        current_action = ""
        fill_slots = []
        n_slots = 0
        current_turn = ""  # user or bot
        while True:
            try:
                if greeting == False:
                    greeting = True
                    speaker.speak(greeting_msg)

                # Listen voice from microphone and generate sentence.
                sentence = listener.listen()
                if sentence == "Error":
                    continue
                # sentence = "Do you have any recommended books written by J k rowling"
                # sentence = "I would like to read books about psychology, do you have any recommendation"
                # sentence = "Do you have any recommended books in psychological category"
                # Check sentence with trained model for dialogue act.
                da_result = da.predict(sentence);
                print("DA type --> ", da_result)
                
                if current_action != "wait_for_slot":
                    curent_intent, similarity_score = parser.infer_intent(sentence)
                    # logging.debug(similarity_score, "-intent: ", curent_intent.__str__())
                    response_statement_key = curent_intent["respond_statement"]

                    if len(response_statement_key) > 0:
                        respond_msg_key = curent_intent["respond_statement"]
                        respond_message = d_manager.get_respond_message(respond_msg_key)
                        speaker.speak(respond_message)
                        current_turn = "user"
                        current_action = curent_intent["next_action"]
                        logging.debug("action: %s", current_action) 
                 
                if len(current_action) > 0 and current_action == "wait_for_slot":
                    required_slots = curent_intent["slots"]
                    n_slots = len(required_slots)
                    if len(fill_slots) < n_slots and current_turn != "user":
                        logging.debug("manage to ask for more info")
                    else:
                        # fill slot
                        # TODO search for slot's value in sentence
                        required_slots.append("call function to get slot")
                        logging.debug("search in ontology")
                 
                elif da_result == "whQuestion" or da_result == "ynQuestion":
                    # Analyze entity in question find subject, predicate, object
                    # Query in ontology by SPARQL 
                    # Generate sentence
                    # parser.get_dependency_parsing(sentence)
                    # parser.generate_response(sentence)
                    
                    # curent_intent = parser.infer_intent(sentence)
                    pass
                
                # If type is end of conversation, stop program.
                elif da_result == "Bye":
                    response_msg = da.respond(sentence)
                    speaker.speak(response_msg)
                    break;
                
                elif da_result == "Greet":
                    # speaker.speak("Hello")
                    # response_msg = da.respond(sentence)
                    # speaker.speak(response_msg)
                    # break;
                    continue
                
                # Problem, when there is no voice come, it returns error.
                # So we handle by continue
                # Continue next loop if Error is returned.
                    
                # response_msg = da.respond(sentence)
                # Call dialogue management and speak
#               # reply_message = dmngr.process(sentence)
                # speaker.speak(response_msg)

            except SystemExit:
                print("ignoring SystemExit")
            except Exception as e:
                print("Exception: " + e.__str__())
 

import config
from chatbot.stt.speech_recognizer import SpeechRecognizer
from chatbot.tts.speech_agent import SpeechAgent
# from chatbot.dialogue.dialogue_manager import DialogueManager
import logging
#from dialogue_act.dialogue_mgt import DialogueActManager
from dialogue_act.dialogue_act import DialogueAct
from chatbot.parser.text_parser import TextParser
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
        parser = TextParser()
        listener, speaker = self.init_agents()

        wakeup_words = ["hey",  "hi", "hello"]
        end_converstion_words = ["bye", "bye bye", "goodbye", "see you"]
        greeting = False
        greeting_msg = "Hello, how may I help you?"
        goodbye_msg = "Hope to see you soon, bye."

        while True:
            try:
                if greeting == False:
                    greeting = True
                    speaker.speak(greeting_msg)

                # Listen voice from microphone and generate text.
                #text = listener.listen()
                #text = "Do you have any recommended books written by J k rowling"
                #text = "I would like to read books about psychology, do you have any recommendation"
                text = "Do you have any recommended books in psychological category"
                # Check text with trained model for dialogue act.
                da_result = da.predict(text);
                print("DA type --> ", da_result)
                
                if da_result == "whQuestion" or da_result == "ynQuestion":
                    # Analyze entity in question find subject, predicate, object
                    # Query in ontology by SPARQL 
                    # Generate sentence
                    parser.get_dependency_parsing(text)
                    parser.generate_response(text)
                
                # If type is end of conversation, stop program.
                if da_result == "Bye":
                    response_msg = da.respond(text)
                    speaker.speak(response_msg)
                    break;
                
                # Problem, when there is no voice come, it returns error.
                # So we handle by continue
                # Continue next loop if Error is returned.
                if text == "Error":
                    continue
                else:
                    
                    response_msg = da.respond(text)
                    # Call dialogue management and speak
#                     reply_message = dmngr.process(text)
                    speaker.speak(response_msg)

            except SystemExit:
                print("ignoring SystemExit")
            except Exception as e:
                print("Exception: " + e.__str__())

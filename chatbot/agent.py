import config
from chatbot.stt.speech_recognizer import SpeechRecognizer
from chatbot.tts.speech_agent import SpeechAgent
# from chatbot.dialogue.dialogue_manager import DialogueManager
import logging
from dialogue_act.dialogue_mgt import DialogueActManager

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
        da = DialogueActManager()

        listener, speaker = self.init_agents()

        bot_name = "angle"
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

                # Listen voice from microphone
                text = listener.listen()

                if text in end_converstion_words:
                    speaker.speak(goodbye_msg)
                    break;

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

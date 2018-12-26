import logging
# Internal library
import subprocess
from abc import abstractmethod

import pyttsx3
# from espeakng import ESpeakNG

# Internal library
import config


class SpeechAgent:
    """
    Factory for creating speech agent
    """

    def __init__(self):
        pass

    def init_agent(self, agent_name):
        """
        See config file for available agents
        :param agent_name:
        """
        if agent_name == config.TTS_PYTTSX3:
            return Pyttsx3Agent()
        # elif agent_name == config.TTS_GTTS:
        #     return OsxSubProcess()
        # elif agent_name == config.TTS_OSX:
        #     return GTTs()
        # elif agent_name == config.TTS_ESPEAK:
        #     return ESpeak()
        else:
            logging.info("Specified agent is not implemented yet.")


class SpeechAgentABC:
    """
    Abstract Based Method class to define required functions of speech agent.
    """

    @abstractmethod
    def speak(self, text):
        pass


class Pyttsx3Agent(SpeechAgentABC):
    engine = None

    def __init__(self):
#         self.engine = pyttsx3.init("nsss", debug=True)
        self.engine = pyttsx3.init(debug=True)
        voices = self.engine.getProperty('voices')
        voice = voices[0]
        voice.age = 5
        self.engine.setProperty("voice", config.SPEAKER_VOICE_NAME)
        voice.languages[0] = config.DEFAULT_LANGUAGE_CODE

    def speak(self, text):
        print("Bot said: {}".format(text))
        # Initialize TTS engine
        # ex. pyttsx3.init(driverName='sapi5')  sapi5 or nsss in mac
        self.engine.say(text)
        self.engine.runAndWait()
        # self.engine.stop()

    # def speak2(self, speech):
    #     engine = pyttsx3.init("nsss", debug=True)
    #     rate = engine.getProperty('rate')
    #     engine.setProperty('rate', rate)
    #     voices = engine.getProperty('voices')
    #     # for voice in voices:
    #     # engine.setProperty('voice', 'english-us')
    #     engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Alex')
    #     # print voice.id
    #     engine.say(speech)
    #     a = engine.runAndWait()  # blocks


class OsxSubProcess:

    def speak(self, text):
        subprocess.call('say ' + text, shell=True)
        print(config.chatbot_name + " said: {}".format(text))


# class ESpeak(SpeechAgentABC):
# 
#     def speak(self, text):
#         esng = ESpeakNG()
#         speech = 'Hello World!'
#         print(speech)
#         esng.pitch = 32
#         esng.speed = 150
#         esng.voice = 'english-us'
#         esng.say(speech)


class GTTs(SpeechAgentABC):

    def speak(self, text):
        pass

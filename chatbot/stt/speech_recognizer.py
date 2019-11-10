#!/usr/bin/env python
__author__ = "Naphatthara P."
__version__ = "1.0.0"
__email__ = "naphatthara.p@gmail.com"
__status__ = "Prototype"

from abc import abstractmethod
import logging

import config
import speech_recognition as sr

# Internal configuration class
logging.getLogger().setLevel(logging.DEBUG)
# Internal lib


class SpeechRecognizerInterface:

    @abstractmethod
    def speech_to_text(self):
        pass


class SpeechRecognizer:

    def __init__(self):
        pass

    def init_recognizer(self, recognizer_name, language_code):
        if recognizer_name == "" or recognizer_name == config.STT_GOOGLE:
            return GoogleRecognizer(language_code)
        else:
            logging.warning("recognizer for {} is not implemented yet".format(
                recognizer_name))


class SpeechRecognizerABC:

    def __init__(self, language_code):
        self.LANGUAGE_CODE = language_code

    @abstractmethod
    def listen(self):
        pass


class GoogleRecognizer(SpeechRecognizerABC):

    wait_timeout_sec = 15

    def listen(self):
        logging.debug("ฺBot is listening...")
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            audio = recognizer.listen(source, self.wait_timeout_sec)

        try:
            speech = recognizer.recognize_google(audio,
                                                 language=config.LANGUAGE_CODE)
            logging.debug(" You said>> " + speech)
            try:
                return speech
            except TypeError:
                print("Error! Could not convert speech to string!")
                return "Error"
        except sr.UnknownValueError:
            # print("UnknownValueError Could not process that audio.")
            return "Error"
        except sr.WaitTimeoutError:
            print("timeout...")
            return "Error Timeout"
        except sr.RequestError as e:
            print("Error! No internet connection to Google Sound Recognizer.")
        return "Error!"


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

    def init_recognizer(self, recognizer_name):
        if recognizer_name == "" or recognizer_name == config.STT_GOOGLE:
            return GoogleRecognizer()
        else:
            logging.warning("recognizer for {} is not implemented yet".format(
                recognizer_name))


class SpeechRecognizerABC:

    @abstractmethod
    def listen(self):
        pass


class GoogleRecognizer(SpeechRecognizerABC):

    wait_timeout_sec = 20

    def listen(self):

        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            audio = recognizer.listen(source, self.wait_timeout_sec)

        try:
            speech = recognizer.recognize_google(audio,
                                                 language=config.DEFAULT_LANGUAGE_CODE)
            logging.debug("You said: " + speech)
            try:
                return speech
            except TypeError:
                print("Error! Could not convert speech to string!")
                return "Error"
        except sr.UnknownValueError:
            print("UnknownValueError Could not process that audio.")
            return "Error"
        except sr.WaitTimeoutError:
            print("timeout...")
            return ""
        except sr.RequestError as e:
            print("Error! No internet connection to Google Sound Recognizer.")
        return "Error!"


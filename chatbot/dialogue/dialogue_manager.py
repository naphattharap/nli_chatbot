from chatbot.parser.text_parser import TextParser
import logging
#  pip install ipython
logging.getLogger().setLevel(logging.DEBUG)


class DialogueManager:

    parser = TextParser()

    def process(self, text):
        doc = self.parser.analyze_text(text)

        reply_message = "Please implement dialog manager"
        return reply_message

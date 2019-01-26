from chatbot.parser.text_parser import TextParser


class Test():

    def test_intents(self):
        tp= TextParser()
        try:
            with open('testFile.csv') as infile:
                for line in infile:
                    sentence =line.split(",")[0]

                    print(tp.infer_intent(sentence))


        except BaseException as e:
            print("Error occurred is:  %s" % str(e))

t = Test()
t.test_intents()
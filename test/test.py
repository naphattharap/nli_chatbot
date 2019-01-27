from chatbot.parser.text_parser import TextParser


class Test():

    def test_intents(self):
        tp = TextParser()
        try:
            with open('testFile.csv') as infile:
                for line in infile:
                    if line != "" and line.strip() != "":
                        sentence = line.split(",")[0]
                        expected_intent = line.split(",")[1].strip()
                        inferred_intent = tp.infer_intent(sentence)
                        if(inferred_intent == expected_intent) == False:
                            print("EEEEEEEEEEEERRRRRRRRRRRRRRRRRRRRRRR")
                            print(sentence)
                            print(inferred_intent == expected_intent, "\texpected: ", expected_intent, "\tinferred: ", inferred_intent)
                            print()
                            print()
                            
                        # print( "\t", tp.infer_intent(sentence))
                    
        except BaseException as e:
            print("Error occurred is:  %s" % str(e))


t = Test()
t.test_intents()

from random import randint

class Nlg():
    "Template language generator"

    def __init__(self):
        self.token = "<$>"
        self.options = []


    def templated(self):
        "ITS NECESSARY THAT THE THE OBJECT THAT CALL THIS METHOD HAS AS ARGUMENT THE INTENT"
        "Read sentences ~ answers file for the corresponding intent, replace token with the sparkql value and return"
        "one randomly"
        try:
            with open('rec_book.txt') as infile:
                self.token = "<$>"
                value = "Harry Potter"
                self.options = []

                for line in infile:
                    # string replace
                    self.options.append(line.replace(self.token,value))
                # select random from the list and return template
                return self.options[randint(0, len(self.options) - 1)]

        except BaseException as e:
            print("Error occurred is:  %s" % str(e))



t = Nlg()
t.templated()
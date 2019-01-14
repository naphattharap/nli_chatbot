from nltk.corpus import switchboard
from nltk import download
from nltk.corpus import nps_chat
import nltk
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.svm import SVC
from nltk.corpus.reader import NPSChatCorpusReader
import os


import glob

"""
install nltk:
    http://www.nltk.org/install.html
        sudo pip install -U nltk
        sudo pip install -U numpy
        $ python
        $ import nltk
        
Troubleshoot:
If nltk.download is not working, do as following.
At terminal back to root folder cd ~/ and run following
/Applications/Python\ 3.6/Install\ Certificates.command
"""
# nltk.download()

#http://aclweb.org/anthology/C18-1300
# download('switchboard')

#switchboard.ensure_loaded()
#switchboard.tagged_discourses()




class DialogueAct:


      
    def __init__(self):
        self.train()

        
    def train(self):
        """ http://www.nltk.org/howto/classify.html """
        # posts = nltk.corpus.nps_chat.xml_posts()[:10000]
        #posts = nltk.corpus.nps_chat.xml_posts()
        
        #path = "../nps_chat/*.xml"
        
        #path = "../nps_chat"
        
        path = "./nps_chat" # call from main.py
        
        #print(glob.glob("./nps_chat"))
        files = os.listdir(path);

        reader = NPSChatCorpusReader(root="./nps_chat", fileids=files)

        
        posts = reader.xml_posts()
        featuresets = [(self.dialogue_act_features(post.text), post.get('class')) for post in posts]
        size = int(len(featuresets) * 0.2)
        train_set, test_set = featuresets[size:], featuresets[:size]
        
        self.classifier = nltk.NaiveBayesClassifier.train(train_set)
        
        
        print("NaiveBays", nltk.classify.accuracy(self.classifier, test_set))
        
        #self.classifier2 = nltk.DecisionTreeClassifier.train(train_set)
        #print("DS", nltk.classify.accuracy(self.classifier2, test_set))
        
        #self.classifier  = SklearnClassifier(SVC(gamma="scale"), sparse=False).train(train_set)

        #print(nltk.classify.accuracy(self.classifier, test_set))
        #clf.fit(X, y)  
        
        chat_utterances = posts
        
        dialogue_acts = ['Accept', 
                         'Bye', 
                         'Clarify', 
                         'Continuer', 
                         'Emotion', 
                         'Emphasis', 
                         'Greet', 
                         'nAnswer', 
                         'Other', 
                         'Reject', 
                         'Statement', 
                         'System', 
                         'whQuestion', 
                         'yAnswer', 
                         'ynQuestion']
    
        for a in dialogue_acts :
            for u in chat_utterances :
                if u.get('class') == a:
                    print("Example of {}: {}".format(a, u.text))
                    break
        return self.classifier
    
    def predict(self, text):
        return self.classifier.classify(self.dialogue_act_features(text))
            
    def dialogue_act_features(self, post):
        features = {}
        for word in nltk.word_tokenize(post):
                features['contains({})'.format(word.lower())] = True
        return features
    
    def word_feat(self, word):
        return dict([(word,True)])
    

    
    # https://github.com/iwcs15-hack/dialog_system/blob/master/using-classifiers.py
    def respond_question(self, text, valence) :
        if valence == 'pos' :
            
            return "I wish I knew."
        else :
            return "That's a tough question."
        
    def respond_other(self, text, valence) :
        return ":P  Well, what next?"
    
    def respond_statement(self, text, valence) :
        if valence == 'pos' :
            return "Great!  Tell me more."
        else :
            return "Ugh.  Is anything good happening?"
        
    def respond_bye(self, text, valence) :
        return "I guess it's time for me to go then."
    
    def respond_greet(self, text, valence) :
        return "Hello"
    
    def respond_reject(self, text, valence) :
        if valence == 'pos' :
            return "OK."
        else :
            return "I still think you should reconsider."
        
    def respond_emphasis(self, text, valence) :
        if valence == 'pos' :
            return '!!!'
        else :
            return ":("
        

    
    def respond(self, text) :
        responses = {'Accept': self.respond_other, 
                     'Bye': self.respond_bye, 
                     'Clarify': self.respond_other, 
                     'Continuer': self.respond_other, 
                     'Emotion': self.respond_other, 
                     'Emphasis': self.respond_emphasis, 
                     'Greet': self.respond_greet, 
                     'nAnswer': self.respond_other, 
                     'Other': self.respond_other,  
                     'Reject': self.respond_reject, 
                     'Statement': self.respond_statement, 
                     'System': self.respond_other, 
                     'whQuestion': self.respond_question, 
                     'yAnswer': self.respond_other, 
                     'ynQuestion': self.respond_question}
        act = self.predict(text)
        print("predict", act)
    #     valence = expt1.classify(text)
        valence = 'pos'
        return responses[act](text, valence)
    
    def test(self):
        
        book_bot = ["Do you have any recommended books written by J k rowling"]
        
        book_bot2 = ["So, do you go to college right now",
                    "Yeaa…",
                    "It is my last year",
                    "You are a, so you’re a senior now",
                    "Yeah",
                    "I’m working on my projects trying to graduate",
                    "Oh, good for you",
                    "Yeah",
                    "That’s great!",
                    "Hello, Good Morning, how can I help you",
                    "I am looking for a new book to read… Can you recommend me one",
                    "Sure What genre do you like the most",
                    "Umm Science - fiction. ",
                    "Something about shapeshifters",
                    "Not really",
                    "Ok, How about witches and warlocks",
                    "Yeah ",
                    "Have you already read Harry Potter",
                    "Nop. Thanks I’ll take a look.",
                    "I’m trying to remember the author of The Lord of the Rings",
                    "The author is J.R. Tolkien",
                    "Is the same one as Harry Potter",
                    "No the author of Harry Potter is J.K. Rowling.",
                    "Ah Ok. So what books has J.R. Tolkien written",
                    "‘The Hobbit or Bilbo's last song",
                    "Hello Chatbot could you recommend any book about psychology",
                    "Do you have any preference for author name or publisher",
                    "No I don’t.",
                    "Would you like to read popular books or new released books",
                    "Popular books.",
                    "We have books in phycology genre named",
                    "The Happiness Hypothesis by Jonathan Heidt and Civilization and Its Discontents by Sigmund Freud and others. Would you like to see more",
                    "No, thanks. Do you have other books written by Sigmund Freud",
                    "Well, there are many books like The EGO and ID, Uncanny, Beyond the Pleasure Principle",
                    "The EGO and ID What is it about",
                    "The id, ego, and super-ego are three distinct yet interacting agents in the psychic apparatus defined in Sigmund Freud's structural model of the psyche. The three parts are the theoretical constructs in terms of whose activity and interaction our mental life is described.",
                    "OK thank you I will take a look",
                    "I hope you like the book."
                    ]
        for i in range(len(book_bot)): 
            print("DA:\t",  self.classifier.classify(self.dialogue_act_features(book_bot[i])), "\t|\t", book_bot[i], "\t|\t", self.respond(book_bot[i]))
            
# o = DialogueAct()
# o.test()    

#!/usr/bin/env python
__author__ = "Naphatthara P."
__version__ = "1.0.0"
__email__ = "naphatthara.p@gmail.com"
__status__ = "Prototype"

from nltk.corpus import switchboard
from nltk import download
from nltk.corpus import nps_chat
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.svm import SVC

import nltk
import os
import logging
import config

# Below source code will download and store nltk_data to local machine
# only for the first run and when the folder does not exist.
# For the 2nd run onwards, it will check only if it is the updated version.
nltk.download('punkt')
from nltk.corpus.reader import NPSChatCorpusReader

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

# http://aclweb.org/anthology/C18-1300
# download('switchboard')

# switchboard.ensure_loaded()
# switchboard.tagged_discourses()

is_trained = False
# when run from main, it should be ./nps_chat


class DialogueAct:
      
    def __init__(self):
        if not is_trained:
            
            self.train()
        
    def train(self):
        """ http://www.nltk.org/howto/classify.html """
        
        files = os.listdir(config.NPS_CORPUS_PATH)
        logging.debug("files: %s", files)
        reader = NPSChatCorpusReader(root=config.NPS_CORPUS_PATH, fileids=files)  
        
        posts = reader.xml_posts()
        featuresets = [(self.dialogue_act_features(post.text), post.get('class')) for post in posts]
        size = int(len(featuresets) * 0.2)
        train_set, test_set = featuresets[size:], featuresets[:size]
        
        self.classifier = nltk.NaiveBayesClassifier.train(train_set)
        accuracy = nltk.classify.accuracy(self.classifier, test_set)
        logging.debug("NaiveBayes Accuracy: %s", accuracy)  # 0.6838618078561287
        
#         clf_ds = nltk.DecisionTreeClassifier.train(train_set)
#         accuracy_2 = nltk.classify.accuracy(clf_ds, test_set)
#         logging.debug("Decision Tree Accuracy: %s", accuracy_2)  
#           
#         svc = SklearnClassifier(SVC(gamma="scale"), sparse=False).train(train_set)
#         accuracy_3 = nltk.classify.accuracy(svc, test_set)
#         logging.debug("Sklearn Accuracy: %s", accuracy_3)  

        # clf.fit(X, y)  
        
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
    
        # Print example of messages
        for a in dialogue_acts :
            for u in chat_utterances :
                if u.get('class') == a:
                    logging.debug("Example of {}: {}".format(a, u.text))
                    break
        return self.classifier
    
    def predict(self, text):
        return self.classifier.classify(self.dialogue_act_features(text))
            
    def dialogue_act_features(self, post):
        features = {}
        for word in nltk.word_tokenize(post):
            features['contains({})'.format(word.lower())] = True
        return features  

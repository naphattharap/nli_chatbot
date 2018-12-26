# pip install spacy
# python -m spacy download en_core_web_sm
# conda install -c conda-forge spacy
# download exact model version (doesn't create shortcut link)
# PyCharm
# python -m spacy download en_core_web_sm-2.0.0 --direct
# python -m spacy download en_core_web_sm
# in case IDE is eClipse run below command at the interpreter
# -m spacy download en_core_web_sm-2.0.0 --direct 
import logging
import spacy
from IPython.display import display, Image
from spacy import displacy


logging.getLogger("dialogue_manager").setLevel(logging.DEBUG)


class TextParser():
    # Load English tokenizer, tagger, parser, NER and word vectors

    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

    def analyze_text(self, text):

        self.doc = self.nlp(text)
        self.print_doc()
        return self.doc

    def print_doc(self):
        # The Token class exposes a lot of word-level attributes.
        print("Token --> ")
        for token in self.doc:
            print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}".format(
                token.text,
                token.idx,
                token.lemma_,
                token.is_punct,
                token.is_space,
                token.shape_,
                token.pos_,
                token.tag_
            ))

        # Find named entities, phrases and concepts
        print("Text and Label --> ")
        for entity in self.doc.ents:
            print("text {} label {}".format(entity.text, entity.label_))

        print("doc.sent --> ")
        for sent in self.doc.sents:
            print(sent)

        # POS
        print("Part Of Speech --> ")
        print([(token.text, token.tag_) for token in self.doc])

        # NER (Name entity recognition)
        print("Name entity recognition --> ")
        for ent in self.doc.ents:
            print(ent.text, ent.label_)

        # Visualize name entity
        print("Visualize entity")
        displacy.render(self.doc, style='ent', jupyter=True)

        print("Dependency parsing --> ")
        for token in self.doc:
            print("{0}/{1} <--{2}-- {3}/{4}".format(
                token.text, token.tag_, token.dep_, token.head.text,
                token.head.tag_))

        print("Dependency tree --> ")
        displacy.render(self.doc, style='dep', jupyter=True,
                        options={'distance': 90})

    def test(self):
        # Test
        # Process whole documents
        text = (u"Hello, do you have any recommended books?")

        parser = TextParser()
        parser.analyze_text(text)
        # Determine semantic similarities
        doc1 = parser.nlp(u"How are you doing?")
        doc2 = parser.nlp(u"Good Morning, how can I help you?")
        similarity = doc1.similarity(doc2)
        print("doc1 : ", doc1.text, "\ndoc2", doc2.text, "\nsimilarity",
              similarity)


a = TextParser()
a.test()

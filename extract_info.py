import nltk
import re
import numpy
from nltk.tag import StanfordNERTagger
from nltk.parse import CoreNLPParser
from nltk.tokenize import RegexpTokenizer
nltk.download('punkt_tab')
nltk.download('words')
nltk.download('maxent_ne_chunker_tab')
nltk.download('averaged_perceptron_tagger_eng')
import speech_recognition as sr

text = open('examples.txt', 'r').read()
#tokenizer = RegexpTokenizer(r'\w+')
text = re.sub(r'[^\x00-\x7F]+', '', text)
#text = re.sub(r'[^\w\s]', '', text)
grammar = r"""
COURSE: {<STUDY>.*<NNP>+}
        {<STUDY>.*<NN>+},
NAME: {<NAME><NNP>+}
        {<NAME><NN>+}"""

def preprocess(text):
    #sentences = nltk.sent_tokenize(text)
    #sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    sentences = [nltk.word_tokenize(text)]
    sentences = [nltk.pos_tag(sentence) for sentence in sentences]
    return sentences



preprocessed_text = preprocess(text)
preprocessed_text = [
    (word, "STUDY") if (word.lower() == "study") | (word.lower == "studies") | (word.lower == "studying") | (word.lower == "course") else (word, tag)
    for (word, tag) in preprocessed_text[0]
]
text1 = []
for (word, tag) in preprocessed_text:
    if ((word == "study") | (word == "studies") | (word == "studying") | (word == "course") | (word == "doing")):
        text1.append((word, "STUDY"))
    elif ((word == "name") | (word == "Im")):
        text1.append((word, "NAME"))
    else:
        text1.append((word, tag))

result = []
cp = nltk.RegexpParser(grammar)

result = cp.parse(text1)

#for sentence in preprocessed_text:
 #   result1 = cp.parse(sentence)
  #  result.append(result1)
#result = cp.parse(preprocessed_text[0])
ne = []
for tree in preprocessed_text:
    #ne2 = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz', 'stanford-ner.jar')
    ne1 = nltk.chunk.ne_chunk(tree)
    ne.append(ne1)

a = 4
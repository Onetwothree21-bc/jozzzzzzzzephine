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

text = open('example2.txt', 'r').read()
#tokenizer = RegexpTokenizer(r'\w+')
text = re.sub(r'[^\x00-\x7F]+', '', text)
#text = re.sub(r'[^\w\s]', '', text)
grammar = r"""
COURSE: {<STUDY>.*<NNP>+}
        {<STUDY>.*<NN>+}
        {<STUDY>.*<COURSE>+},
NAME: {<NAME><NNP>+}
        {<NAME><NN>+}"""

courses_list = [
    "architecture", "biomed", "biology", "bio", "business", "management", "chem eng", "chemistry", "civil eng", "computer science", "cs", "electrical eng", "ee", "engineering", "english", "history", "maths", "mathematics", "medicine", "physics", "psychology", "social science", "sociology", "statistics", "MSDS", "economics", "econometrics", "finance", "accounting", "marketing", "operations research", "data science", "artificial intelligence", "machine learning", "deep learning", "natural language processing", "computer vision", "cybersecurity", "software engineering", "web development", "mobile app development", "game development", "cloud computing", "big data", "blockchain", "cryptography", "econ", "mech eng", "languages", "physics", "politics", "sports science", "sport management"
]






def preprocess(text):
    #sentences = nltk.sent_tokenize(text)
    #sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    sentences = []
    for line_number, line in enumerate(text.splitlines()):
        id = line.split(':')[0]
        line = line.split(':')[1]
        sentence = nltk.word_tokenize(line)
        sentence = nltk.pos_tag(sentence)
        sentence2 = []
        for word, tag in sentence:
            sentences.append((word, tag, id))
        #sentences.append(sentence2)
    #sentences = [nltk.word_tokenize(text)]
    #sentences = [nltk.pos_tag(sentence) for sentence in sentences]
    return sentences



preprocessed_text = preprocess(text)
#preprocessed_text = [
#    (word, "STUDY") if (word.lower() == "study") | (word.lower == "studies") | (word.lower == "studying") | (word.lower == "course") else (word, tag)
#    for (word, tag, id) in preprocessed_text[0]
#]
text1 = []
for (word, tag, id) in preprocessed_text:
    if ((word == "study") | (word == "studies") | (word == "studying") | (word == "course") | (word == "doing")):
        text1.append((word, "STUDY", id))
    elif ((word == "name") | (word == "Im")):
        text1.append((word, "NAME", id))
    elif (word in courses_list):
        text1.append((word, "COURSE", id))
    else:
        text1.append((word, tag, id))

result = []
cp = nltk.RegexpParser(grammar)

result = cp.parse(text1)

names = {}
for subtree in result.subtrees():
    if subtree.label() == 'NAME':
        names[subtree.leaves()[1][2]] = subtree.leaves()[1][0]  # Store the ID as the value


courses = {}
for subtree in result.subtrees():
    if subtree.label() == 'COURSE':
        course = ""
        for i in range(1, len(subtree.leaves())):
            course += subtree.leaves()[i][0] + " "
        courses[subtree.leaves()[1][2]] = course.strip()  # Store the ID as the value
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
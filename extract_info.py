import string
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


def preprocess(text):
        #sentences = nltk.sent_tokenize(text)
        #sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
        sentences = []
        for line in text.splitlines():
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


def main():
    text = open('examples.txt', 'r').read()
    #tokenizer = RegexpTokenizer(r'\w+')
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    #text = re.sub(r'[^\w\s]', '', text)
    grammar = r"""
    COURSE: {<STUDY>.*<COURSE>+}
    NAME: {<NAME><NNP>}
    NAME: {<NAME><.*><NNP>}
    NAME: {<NAME><NN>}"""

    courses_list = [
        "architecture", "biomed", "biology", "bio", "business", "management", "chem", "chemistry", "civil", "computer science", "computer", "science", "cs", "electrical", "ee", "engineering", "eng", "english", "history", "maths", "mathematics", "medicine", "physics", "psychology", "social", "sociology", "statistics", "MSDS", "economics", "econometrics", "finance", "accounting", "marketing", "econ", "mech", "languages", "physics", "politics", "sports", "sport"
    ]

    preprocessed_text = preprocess(text)
    text1 = []
    for (word, tag, id) in preprocessed_text:
        if ((word == "study") | (word == "studies") | (word == "studying") | (word == "course") | (word == "doing") | (word == "do")):
            text1.append((word, "STUDY", id))
        elif ((word == "name") | (word == "Im")):
            text1.append((word, "NAME", id))
        elif (word.lower() in courses_list):
            text1.append((word, "COURSE", id))
        elif (word not in string.punctuation):
            text1.append((word, tag, id))

    cp = nltk.RegexpParser(grammar)
    parsed_text = cp.parse(text1)

    names = {}
    for subtree in parsed_text.subtrees():
        if subtree.label() == 'NAME':
            names[subtree.leaves()[-1][2]] = subtree.leaves()[-1][0]  # Store the ID as the key and the name as the value
    names = {key: names[key] for key in sorted(names)}  # Sort by key (id)

    courses = {}
    for subtree in parsed_text.subtrees():
        if subtree.label() == 'COURSE':
            course = ""
            for i in range(1, len(subtree.leaves())):
                course += subtree.leaves()[i][0] + " "
            courses[subtree.leaves()[1][2]] = course.strip()  # Store the ID as the key and the course as the value

    output = []
    for key in names.keys():
        output.append({
            "id": key,
            "name": names[key],
            "course": courses.get(key, "")
        })
    return output

    a = 4

main()
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 16:08:03 2019

@author: Minita.m
"""
import numpy as np
import json
import nltk
import operator
import os
import pickle
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

lmtzr = WordNetLemmatizer()
import time
from nltk import word_tokenize
from nltk.corpus import stopwords

stop = set(stopwords.words('english'))
from string import punctuation

# probability threshold

ERROR_THRESHOLD = 0.0
# load our calculated synapse values
synapse_file = r'C:/aics_deployment/text_projects/ICICI_Email_Analytics/ICICI_Email_Analytics/synapses.json'
with open(synapse_file) as data_file:
    synapse = json.load(data_file)
    synapse_0 = np.asarray(synapse['synapse0'])
    synapse_1 = np.asarray(synapse['synapse1'])

words = r'C:/aics_deployment/text_projects/ICICI_Email_Analytics/ICICI_Email_Analytics/words'
classes = r'C:/aics_deployment/text_projects/ICICI_Email_Analytics/ICICI_Email_Analytics/classes'

with open(words, "rb") as wp:  # Unpickling
    words = pickle.load(wp)
with open(classes, "rb") as cp:  # Unpickling
    classes = pickle.load(cp)


def rm_stopword(document):
    val = [i for i in document.lower().split() if i not in stop]
    return " ".join(val)


# compute sigmoid nonlinearity
def sigmoid(x):
    output = 1 / (1 + np.exp(-x))
    return output


# convert output of sigmoid function to its derivative
def sigmoid_output_to_derivative(output):
    return output * (1 - output)


def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)

    return (np.array(bag))


def think(sentence, show_details=False):
    x = bow(sentence.lower(), words, show_details)
    if show_details:
        print("sentence:", sentence, "\n bow:", x)
    # input layer is our bag of words
    l0 = x
    # matrix multiplication of input and hidden layer
    l1 = sigmoid(np.dot(l0, synapse_0))
    # output layer
    l2 = sigmoid(np.dot(l1, synapse_1))
    return l2


def stemSentence(sentence):
    token_words = word_tokenize(sentence)
    token_words
    stem_sentence = []
    for word in token_words:
        stem_sentence.append(lmtzr.lemmatize(word))
        stem_sentence.append(" ")
    return "".join(stem_sentence)


def strip_punctuation(doc):
    return ''.join(c for c in doc if c not in punctuation)


def classify(sentence, show_details=False):
    finaldict = {}
    sentence = sentence.lower()
    sentence = stemSentence(sentence)
    sentence = rm_stopword(sentence)
    sentence = strip_punctuation(sentence)

    # print("Processed sentece:", sentence)
    nndict = {}
    results = think(sentence, show_details)
    results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_results = [[classes[r[0]], r[1]] for r in results]
    # print ("%s \n classification: %s" % (sentence, return_results))
    # return return_results

    for i in range(0, len(return_results)):
        if str(return_results[i][0]).strip() in nndict:
            val = float(return_results[i][1])
            sum = val + float(nndict[str(return_results[i][0]).strip()])
            nndict[str(return_results[i][0]).strip()] = sum
        else:
            nndict[str(return_results[i][0]).strip()] = float(return_results[i][1])
    sorted_x = sorted(nndict.items(), key=operator.itemgetter(1), reverse=True)
    # return (list(sorted_x[0]))

    # n = 3

    

    # print(sorted_x[0][0])
    # print(sorted_x[1][0])
    # finaldict[sorted_x[0][0]] = sorted_x[0]
    # finaldict[sorted_x[1][0]] = (n * 0.5)

    # print(finaldict)
    # print(list(sorted_x[0]))
    if sorted_x[0][1] >= 0.70:
        finaldict['CLASS'] = (list(sorted_x[0]))

        lst = (list(sorted_x[0])[0])
        
        #ddxxprint(lst)

    else:
        #finaldict['CLASS'] = ['Un Classified', 0.0]

        lst = "Un Classified"

    return lst

# if __name__ == "__main__":
    

#     text = "FIR reported in this transaction"

#     print(classify(text))


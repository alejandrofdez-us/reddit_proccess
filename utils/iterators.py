# coding=utf-8
import os
import codecs
import utils.preprocessUtilities as preprocess
from nltk.corpus import stopwords as nltkstop

class MyDocumentsIterator(object):
    '''
    Created on 26 may 2017

    Clase para implementar un iterable de documentos: para cada archivo, devuelve una lista de palabras

    @author: F. Javier Ortega
    '''
    def __init__(self, path):
        self.path = path

    def __iter__(self):
        for filename in os.listdir(self.path):
            yield [word for line in codecs.open(self.path + filename, 'r', 'utf-8') for sent in map(preprocess.limpia,preprocess.tokeniza_frases(line.lower())) for word in preprocess.tokeniza(sent)]


class MyDocumentsStopWordsIterator(object):
    '''
    Created on 26 may 2017

    Clase para implementar un iterable de documentos: para cada archivo, devuelve una lista de palabras, eliminando las stopwords del idioma que le indiquemos (por defecto inglés)

    @author: F. Javier Ortega
    '''

    def __init__(self, path, language="english"):
        self.path = path
        self.stopwords = set(nltkstop.words(language))

    def __iter__(self):
        for filename in os.listdir(self.path):
            yield [word for line in codecs.open(self.path + filename, 'r', 'utf-8') for sent in map(preprocess.limpia,preprocess.tokeniza_frases(line.lower())) for word in preprocess.tokeniza(sent) if word not in self.stopwords]



class MySentenceIterator(object):
    '''
    Created on 26 may 2017

    Clase para implementar un iterable de frases: dado un archivo, devuelve una lista de palabras por cada frase del archivo

    @author: F. Javier Ortega
    '''

    def __init__(self, file):
        self.file = file

    def __iter__(self):
        for line in codecs.open(self.file, 'r', 'utf-8'):
            yield [word for sentence in map(preprocess.limpia,preprocess.tokeniza_frases(line)) for word in preprocess.tokeniza(sentence)]
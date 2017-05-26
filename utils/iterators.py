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
            yield [word for line in codecs.open(filename, 'r', 'utf-8') for word in line.lower().split()]


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
            yield [word for line in codecs.open(filename, 'r', 'utf-8') for word in line.lower().split() if word not in self.stopwords]
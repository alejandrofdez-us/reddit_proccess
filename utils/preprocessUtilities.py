# coding=utf-8
import re
import gensim
import nltk.data
from nltk.tokenize import word_tokenize

LANGUAGE = "english"
tokenizer = nltk.data.load('tokenizers/punkt/' + LANGUAGE + '.pickle')

def limpia(oracion):
    """
    Dada una oración, elimina caracteres no deseados, URL's, números...
    """
    #oracion = re.sub(r"(http[s]?://)?([0-9a-zA-Z/\.\-\+_\?&;=%]+)(\s)", r"URL", oracion)  # Asignar tokens a las URLS
    oracion = re.sub(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_ @.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", r"URL", oracion)
    oracion = re.sub(r"&gt;", r" ", oracion)
    oracion = re.sub(r"&lt;", r" ", oracion)
    oracion = re.sub(r"\.com", r" ", oracion)
    oracion = re.sub(r"[^0-9a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]", " ", oracion)  # Repasar si falta algún carácter latino
    oracion = re.sub(r"(\s)([0-9\.]+)(\s)", r"\1DIGITO\3", oracion)

    return oracion


def tokeniza_frases(texto):
    return tokenizer.tokenize(texto)


def tokeniza(oracion):
    #return gensim.utils.tokenize(oracion)
    return [w for w in word_tokenize(oracion)]
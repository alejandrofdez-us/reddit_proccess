# coding=utf-8
import os
import codecs
import nltk
from nltk.corpus import stopwords
from utils.tiempos import Timer
from utils.iterators import MyDocumentsIterator
from utils import preprocessUtilities as preprocess

globalPath = "./resources/Bodies/"

tags = set(["NN", "NNS", "NP", "V", "VB", "VBZ", "VBG", "VBP"])
stopws = set(stopwords.words("english"))


def countWordFrequencies(sentences):
    '''
    Computes the frequency distribution of words within a document (list of sentences), filtering by tags and stopwords
    :param text_file: 
    :return: 
    '''
    total_words = []
    for sentence in sentences:
        words = preprocess.tokeniza(sentence)
        pos = nltk.pos_tag(words)
        pos_by_tags = [word for word, tag in pos if tag in tags and word not in stopws]
        total_words.extend(pos_by_tags)
    return nltk.FreqDist(total_words)  # print(fdist.most_common(50))


def saveFreqDist(freqdist, outputFile, mostCommon=50):
    '''
    Saves the top-N words of a freqDist to disk
    
    :param freqdist: 
    :param outputFile: 
    :param mostCommon: 
    :return: 
    '''
    file = codecs.open("./resources/fdists/"+outputFile, 'w', 'utf-8')
    for tuple in freqdist.most_common(mostCommon):
        file.write("%s, %s\n"%(str(tuple[0]), str(tuple[1])))
    file.close()


'''
    MAIN
'''

# TODO Consideramos 1 documento = 1 franja = 1 txt
# TODO Modelo TF/IDF de documentos
# TODO Modelo LSA, HDP, LDA de documentos
# TODO Modelo doc2vec de documentos

#globalSentences=[]
totalFiles = len(os.listdir(globalPath))
count = 0;
print("-> Comenzando a procesar cada archivo del corpus")
reloj = Timer()
reloj.start_timer()

for textFilename in os.listdir(globalPath):
    count+=1
    print("\t-> Procesando archivo: %s (%d de %d)"%(textFilename, count, totalFiles))

    text_file = codecs.open(globalPath+textFilename, "r", "utf-8")
    #text_file = codecs.open(globalPath+"BodiesReddit-60minutes-2009-02-01 01:00:00.txt", "r", "utf-8"

    # Para cada franja horaria, tokenizo en frases
    sentences = [map(preprocess.limpia, preprocess.tokeniza_frases(line)) for line in text_file]
    sentences = [item for sent in sentences for item in sent]

    # Vamos acumulando todas las frases de todas las franjas horarias
#    texto=""
#    for s in sentences:
#        texto += " "+s
#    globalSentences.append(texto)

    # Contamos las frecuencias de palabras para cada franja horaria
    fd_file = countWordFrequencies(sentences)
    # Guardamos las frecuencias de cada archivo en un archivo de tuplas
    saveFreqDist(fd_file, textFilename+".fdist", mostCommon=500)

    text_file.close()

reloj.stop_timer()
print("-> Fin del procesamiento archivo a archivo.")
print("\t-> Tiempo transcurrido: %s\n"%(reloj.display_time()))

print("-> Procesando corpus completo...")
reloj.start_timer()
# contamos las frecuencias de palabras para el corpus completo
fdist = countWordFrequencies(MyDocumentsIterator(globalPath))

# Guardamos las frecuencias del corpus en un archivo de tuplas
saveFreqDist(fdist, "global.fdist", mostCommon=500)

reloj.stop_timer()
print("-> Fin del procesamiento del corpus completo.")
print("\t-> Tiempo transcurrido: %s\n"%(reloj.display_time()))




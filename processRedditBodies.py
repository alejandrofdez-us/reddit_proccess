# coding=utf-8
import os
import codecs

from gensim import corpora, models

from utils.tiempos import Timer
from utils.iterators import MyDocumentsIterator, MySentenceIterator

globalPath = "./resources/Bodies/"

def countWordFrequencies(sentences):
    '''
    Computes the frequency distribution of words within a document (list of sentences), filtering by tags and stopwords
    :param sentences: Iterador sobre listas de cadenas
    :return: 
    '''
    dictionary = corpora.Dictionary(sentences)
    corpus = [dictionary.doc2bow(text) for text in sentences]
    tfidf = models.TfidfModel(corpus)

    return tfidf, dictionary, corpus


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

# Consideramos 1 documento = 1 franja = 1 txt
totalFiles = len(os.listdir(globalPath))
count = 0
print("-> Comenzando a procesar cada archivo del corpus")
reloj = Timer()
reloj.start_timer()

for textFilename in os.listdir(globalPath):
    count+=1
    print("\t-> Procesando archivo: %s (%d de %d)"%(textFilename, count, totalFiles))
    # Contamos las frecuencias de palabras para cada franja horaria
    fd_file, dictionary, corpus = countWordFrequencies(MySentenceIterator(globalPath + textFilename))
    # Guardamos las frecuencias de cada archivo en un archivo de tuplas
    corpora.MmCorpus.serialize('./resources/fdists/'+textFilename+'.mm', corpus)
    dictionary.save('./resources/fdists/'+textFilename+ '.dict')
    fd_file.save('./resources/fdists/'+textFilename+ '.fdist')

    # Esto en realidad no hace mucha falta...
    model = fd_file[corpus]
    model.save('./resources/fdists/'+textFilename+ '.fdist.model')

reloj.stop_timer()
print("-> Fin del procesamiento archivo a archivo.")
print("\t-> Tiempo transcurrido: %s\n"%(reloj.display_time()))

print("-> Procesando corpus completo...")
reloj.start_timer()

# contamos las frecuencias de palabras para el corpus completo
fd_file, dictionary, corpus = countWordFrequencies(MyDocumentsIterator(globalPath))

# Guardamos las frecuencias de cada archivo en un archivo de tuplas
corpora.MmCorpus.serialize('./resources/fdists/global.mm', corpus)
dictionary.save('./resources/fdists/global.dict')
fd_file.save('./resources/fdists/global.fdist')

reloj.stop_timer()
print("-> Fin del procesamiento del corpus completo.")
print("\t-> Tiempo transcurrido: %s\n"%(reloj.display_time()))





# Modelos "clásicos" aplicables a las tablas de frecuencias para obtener topics
# TODO Eliminar el uso de FreqDist de nltk y utilizar el de Gensim (como se ve a continuación)
# TODO Modelo LSA, HDP, LDA de documentos
#dictionary = corpora.Dictionary(MyDocumentsIterator(globalPath))
#dictionary.save(file +'.dict')
#corpus = [dictionary.doc2bow(text) for text in documents]
#corpora.MmCorpus.serialize(file+'.mm', corpus)
#
#tfidf = models.TfidfModel(corpus)
# corpus_tfidf = tfidf[corpus]
#
# # MODELS for topic detection
# #model = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=5)
# #model = models.HdpModel(corpus_tfidf, id2word=dictionary)
# model = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=100)
# model.print_topics(5)
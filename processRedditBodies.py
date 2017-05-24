# coding=utf-8
import os
import codecs
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from gensim.models import word2vec
import utils.preprocessUtilities as preprocess

globalPath = "./resources/Bodies/"

tags = set(["NN", "NNS", "NP", "V", "VB", "VBZ", "VBG", "VBP"])
stopws = set(stopwords.words("english"))

# Word2Vec: Set values for various parameters
NUM_FEATURES = 300    # Word vector dimensionality
MIN_WORD_COUNT = 50   # Minimum word count
NUM_WORKERS = 2       # Number of threads to run in parallel
CONTEXT = 10          # Context window size
DOWNSAMPLING = 1e-3   # Downsample setting for frequent words

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


def word2vecTrain(sentences, output_file=None):
    '''
    Trains a word2vec model given a list of documents 
    :param sentences:  List of documents as lists of strings
    :param output_file: output file for the model. Not saved if is None
    :return: 
    '''
    # Initialize and train the model (this will take some time)
    print("Training model...")
    model = word2vec.Word2Vec(sentences, workers=NUM_WORKERS,
                              size=NUM_FEATURES, min_count=MIN_WORD_COUNT,
                              window=CONTEXT, sample=DOWNSAMPLING)

    # If you don't plan to train the model any further, calling
    # init_sims will make the model much more memory-efficient.
    model.init_sims(replace=True)

    if output_file == None:
        print("Saving model to file: %s"%output_file)
        # It can be helpful to create a meaningful model name and
        # save the model for later use. You can load it later using Word2Vec.load()
        model.save(output_file)

    return model


'''
    MAIN
'''

# TODO Consideramos 1 documento = 1 franja = 1 txt
# TODO Modelo TF/IDF de documentos
# TODO Modelo LSA, HDP, LDA de documentos
# TODO Modelo doc2vec de documentos

globalSentences=[]
for textFilename in os.listdir(globalPath):
    # TODO usar iteradores sobre archivos, documentos y frases?
    text_file = codecs.open(globalPath+textFilename, "r", "utf-8")
    #text_file = codecs.open(globalPath+"BodiesReddit-60minutes-2009-02-01 01:00:00.txt", "r", "utf-8")
    fdist = FreqDist([])
    for line in text_file:
        sentences = map(preprocess.limpia, preprocess.tokeniza_frases(line))
        globalSentences.extend(sentences)
        # TODO ahorrarnos tanto update de las freqdists
        fd = countWordFrequencies(sentences)
        fdist.update(fd)
    # TODO ¿Qué hacemos con las frecuencias de cada archivo?
    text_file.close()
    print(fdist.most_common(50))



#word2vec_model = train(globalSentences, globalPath+"w2v.model")

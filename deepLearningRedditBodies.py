# coding=utf-8
from gensim.models import word2vec, doc2vec
import utils.iterators as iterators


# Word2Vec: Set values for various parameters
NUM_FEATURES = 300    # Word vector dimensionality
MIN_WORD_COUNT = 50   # Minimum word count
NUM_WORKERS = 2       # Number of threads to run in parallel
CONTEXT = 10          # Context window size
DOWNSAMPLING = 1e-3   # Downsample setting for frequent words

globalPath = "./resources/Bodies/"


def word2vecTrain(sentences, output_file=None):
    '''
    Trains a word2vec model given a list of documents 
    :param sentences:  List of documents as lists of strings
    :param output_file: output file for the model. Not saved if is None
    :return: 
    '''
    # Initialize and train the model (this will take some time)
    print("Training word2vec model...")
    model = word2vec.Word2Vec(sentences, workers=NUM_WORKERS,
                              size=NUM_FEATURES, min_count=MIN_WORD_COUNT,
                              window=CONTEXT, sample=DOWNSAMPLING)
    # If you don't plan to train the model any further, calling
    # init_sims will make the model much more memory-efficient.
    model.init_sims(replace=True)

    if output_file != None:
        print("Saving model to file: %s"%output_file)
        # It can be helpful to create a meaningful model name and
        # save the model for later use. You can load it later using Word2Vec.load()
        model.save(output_file)

    return model


def doc2vecTrain(docs, output_file=None):
    '''
    Trains a doc2vec model given a list of documents 
    :param docs:  List of documents as lists of strings
    :param output_file: output file for the model. Not saved if is None
    :return: 
    '''
    # Initialize and train the model (this will take some time)
    print("Training doc2vec model...")
    model = doc2vec.Doc2Vec(docs, workers=NUM_WORKERS,
                              size=NUM_FEATURES, min_count=MIN_WORD_COUNT,
                              window=CONTEXT, sample=DOWNSAMPLING)
    # If you don't plan to train the model any further, calling
    # init_sims will make the model much more memory-efficient.
    model.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)

    if output_file != None:
        print("Saving model to file: %s"%output_file)
        # save the model for later use. You can load it later using Doc2Vec.load()
        model.save(output_file)

    return model


'''
    MAIN
'''

# Training
#doc2vec_model = doc2vecTrain(iterators.MyDocumentsIteratorDoc2Vec(globalPath) , "./resources/deeplearning/doc2vec.model")

# Loading model
doc2vec_model = doc2vec.Doc2Vec.load("./resources/deeplearning/doc2vec.model");

print(doc2vec_model.docvecs.most_similar('BodiesReddit-60minutes-2009-02-01 00:00:00.txt'))
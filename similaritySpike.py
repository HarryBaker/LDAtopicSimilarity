__author__ = 'Harry Baker'

import gensim
import numpy as np
import sympy
from operator import itemgetter
from gensim import matutils
from gensim import models
from topic2vec import topic2vec
from gensim.corpora import Dictionary
import json
import cPickle as pickle

from similaritySuite import similaritySuite



import math

from math import log10, floor

from LDATopicSimilarity import TopicSimilarity

from modelTranslator import Translator

from topic2vec import topic2vec

#import batch.clusters_runner as cr

if __name__ == '__main__':
    #shrew = cr.doLDA_EEBO(searchterm='Shrew',
                     # ntopics=50,
                     # npasses=100)

    #models.LdaModel.save('/Users/loaner/Documents/Renncode_2016/SKPN/py-server/Shrew')



    tragedyModel = models.LdaModel.load('/Users/loaner/Documents/Renncode_2016/SKPN/py-server/LDA Tragedy')
    comedyModel = models.LdaModel.load('/Users/loaner/Documents/Renncode_2016/SKPN/py-server/LDA Screw')

    #schrewVec = models.Word2Vec.load("/Users/loaner/Documents/Renncode_2016/SKPN/py-server/Shrew_word2vecClass")

    print "Shrew"
    #print schrewVec.most_similar("shrew")
    #I want to combine these into the same class
    #tragSimilarity = TopicSimilarity(tragedyModel)
    #tragArrayConstant = tragSimilarity.HessingerDistancePrune("Constant")
    #tragArrayDynamic = tragSimilarity.HessingerDistancePrune("Dynamic")




    #comSimilarity = TopicSimilarity(comedyModel)
    #comArrayConstant = comSimilarity.HessingerDistancePrune("Constant")
    #comArrayDynamic = comSimilarity.HessingerDistancePrune("Dynamic")


    #with open('trag_data_const.json', 'w') as f:
    #    json.dump(tragArrayConstant, f)

    #with open('com_data_const.json', 'w') as f:
    #    json.dump(comArrayConstant, f)

    #with open('trag_data_dyn.json', 'w') as f:
    #    json.dump(tragArrayDynamic, f)

    #with open('com_data_dynt.json', 'w') as f:
    #    json.dump(comArrayDynamic, f)


    root = "/Users/loaner/Documents/Renncode_2016/SKPN/py-server/batch/topicSimilarity/"
    sentRoot = '/Users/loaner/Documents/Renncode_2016/SKPN/py-server/'

    with open(sentRoot + 'topic2vecSentancesSchrew.json', 'r') as f:
        schrewSentances = json.load(f)

    with open(root + 'trag_data_const.json', 'r') as f:
        tragDataConst = json.load(f)

    with open(root + 'com_data_const.json', 'r') as f:
        comDataConst = json.load(f)

    with open(root + 'trag_data_dyn.json', 'r') as f:
        tragDataDyn = json.load(f)

    with open(root + 'com_data_dynt.json', 'r') as f:
        comDataDyn = json.load(f)



    #find how to save this
    #bothModels = Translator(tragedyModel, comedyModel)
    #x = bothModels.mostCommonTopics("Model1", 15)

    #y = topic2vec(tragedyModel)
    #aa = topic2vec(schrewSentances, comedyModel, flag = False, filename= "Schrew-50-3-10", size=50,window=3,mincount=10)
    #ab = topic2vec(schrewSentances, comedyModel, flag = False, filename= "Schrew-100-3-10",  size=100,window=3,mincount=10)
    #ac = topic2vec(schrewSentances, comedyModel, flag = False, filename= "Schrew-200-3-10", size=200,window=3,mincount=10)
    #ad = topic2vec(schrewSentances, comedyModel, flag = False, filename= "Schrew-300-3-10", size=300,window=3,mincount=10)
    #ae = topic2vec(schrewSentances, comedyModel, flag = False, filename= "Schrew-600-3-10",  size=600,window=3,mincount=10)

    #ba = topic2vec(schrewSentances, comedyModel, flag = False, filename= "Schrew-50-5-10", size=50,window=5,mincount=10)
    #bb = topic2vec(schrewSentances, comedyModel, flag = False, filename= "Schrew-100-5-10",  size=100,window=5,mincount=10)
    #bc = topic2vec(schrewSentances, comedyModel, flag = False, filename= "Schrew-200-5-10", size=200,window=5,mincount=10)
    #bd = topic2vec(schrewSentances, comedyModel, flag = False, filename= "Schrew-300-5-10", size=300,window=5,mincount=10)
    #be = topic2vec(schrewSentances, comedyModel, flag = False, filename= "Schrew-600-5-10",  size=600,window=5,mincount=10)

    #ca = topic2vec(schrewSentances, comedyModel, flag = False, filename= "Schrew-50-7-10", size=50,window=7,mincount=10)
    #cb = topic2vec(schrewSentances, comedyModel, flag = False, filename= "Schrew-100-7-10",  size=100,window=7,mincount=10)
    #cc = topic2vec(schrewSentances, comedyModel, flag = False, filename= "Schrew-200-7-10", size=200,window=7,mincount=10)
    #cd = topic2vec(schrewSentances, comedyModel, flag = False, filename= "Schrew-300-7-10", size=300,window=7,mincount=10)
    #ce = topic2vec(schrewSentances, comedyModel, flag = False, filename= "Schrew-600-7-10",  size=600,window=7,mincount=10)



    #x = topic2vec(schrewSentances, comedyModel, flag = False, filename= "Schrew-50-3-10", size=50,window=3,mincount=10)

    #simSuite = similaritySuite(comedyModel, schrewSentances)
    simSuite = TopicSimilarity(comedyModel,schrewSentances, flag=False, filename="Schrew-600-5-10")

    with open('tragedySimilaritySuite', 'wb') as output:
        pickle.dump(simSuite.findSimilarity(45), output, pickle.HIGHEST_PROTOCOL)

    with open('tragedySimilaritySuite', 'rb') as input:
        simSuite = pickle.load(input)





    #simSuite.findSimilarity(45)
    #dictionary = x.dictionary

    #u = be.topic2vec.similarity('u8','u30')
    #v = be.topic2vec.similarity('u9','u30')

    print "Comparison Testing"

    #y = comedyModel[dictionary.doc2bow(["schrew"])]
    #print y[-1]
    #print aa.mostSimilarTopic('schrew')

    print "done"
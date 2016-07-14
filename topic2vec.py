__author__ = 'loaner'
import gensim
import numpy as np
import sympy
from operator import itemgetter
from gensim import matutils, models
import math
import random
import string
from gensim.corpora import Dictionary

#Find out how to save these objects
#creates a topic2vec model, which is basically just a word2vec model that iterates through each sentance for every word
#
class topic2vec:
    def __init__(self, sentances, ldaModel, flag, filename, size, window, mincount):

        self.sentances = sentances
        self.ldaModel = ldaModel
        self.filename = filename
        self.size = size
        self.window = window
        self.mincount = mincount


        #word = self.sentances[0][0]
        self.permuteSentances = []


        self.dictionary = gensim.corpora.Dictionary.load('/Users/loaner/Documents/Renncode_2016/SKPN/py-server/comTragDict')

        self.dictID = self.dictionary.token2id


        if flag:
            print "starting variation"
            print "There are %d many sentances" % len(self.sentances)
            self.sentanceVariation(self.sentances)

            random.shuffle(self.permuteSentances)
            x = self.permuteSentances

            self.topic2vec = models.Word2Vec(self.permuteSentances, size=self.size, window=self.window, min_count=self.mincount, workers=2)
            self.topic2vec.save(self.filename)

            random.shuffle(self.sentances)
            self.word2vec = models.Word2Vec(self.sentances, size=self.size, window=self.window, min_count=3, workers=2)
            self.topic2vec.save(self.filename + "_w2v")




        #self.word2vec = models.Word2Vec.load('Shrew_word2vecClass')
        self.topic2vec = models.Word2Vec.load(self.filename)
        #self.word2vec = models.Word2Vec.load(self.filename + "_w2v")






        self.ldaTopics = []
        for x in range(0,50):
            self.ldaTopics.append(self.ldaModel.show_topic(x))

        self.topicVecs = []
        for x in range(0,50):
            self.topicVecs.append(self.topic2vec.most_similar(positive=["u" + str(x)]))

        topics = self.topicVecs
        lda = self.ldaTopics
        print self.filename + "is finished"
        #Outer loop
        #for sentance in self.sentances:
        #    #total for each sentance variation
           # sentanceVec = []
         #   for word in sentance:
         #       if word in x:
         #           wordBow = self.dictionary.doc2bow([word])
         #           topic = self.ldaModel[wordBow]
                    #tokenize?
          #          likelyTopic = topic[-1][0]
         #           sent

    #Make recursive?
    #pair word with index
    def sentanceVariation(self, sentances):
        totalVariation = []
        i = 0
        for sentance in sentances:
            print i
            i+= 1
            sentancePermute = self.sentanceVariationHelper1(sentance)
            totalVariation.append(sentancePermute)

        return totalVariation


    #THIs is the problem. how to convert paragraphs into actual sentances
    def sentanceVariationHelper1(self,sentance):
        sentanceVariation = []
        index = 0
        for word in sentance:
            wordPermute = self.sentanceVariationHelper2(word, index, sentance)
            #print wordPermute
            sentanceVariation.append(wordPermute)
            index += 1

        return sentanceVariation


    def sentanceVariationHelper2(self, word, index, sentance):
        sentancePermute = list(sentance)


        if word in self.dictID:
            wordBow = self.dictionary.doc2bow([word])
            topic = self.ldaModel[wordBow]
            likelyTopic = topic[-1][0]
            sentancePermute[index] = "u" + str(likelyTopic)



        #for word in sentance:
        #    if word in self.dictID and flag == False:
        #        wordBow = self.dictionary.doc2bow([word])
        #        topic = self.ldaModel[wordBow]
        #        likelyTopic = topic[-1][0]
        #        sentancePermute.append(likelyTopic)
        #        flag = True#
#
#            else:
#                sentancePermute.append(word)
        self.permuteSentances.append(sentancePermute)
        return sentancePermute


    def mostSimilarTopic(self, word):
        score = (0,0)
        #wordBow = self.dictionary.doc2bow([word])

        if word in self.dictID:
            for x in range(0,50):
                newScore = self.topic2vec.similarity("u" + word, "u" + str(x))
                if newScore > score[0]:
                    score[0] = newScore
                    score[1] = "u" + str(x)
        else:
            print "Word %s not in dictionary" % word

        return score












__author__ = 'loaner'
import gensim
import numpy as np
import sympy
from operator import itemgetter
from gensim import matutils
import math
import json



from LDATopicSimilarity import TopicSimilarity



#This class compares topics across models. Still in development, and only works for cosine sim and hessinger
#I dropped this to work on word2vec stuff, so it's pretty rusty. The basic idea is that it creates a combined
#dictionary of the two models. I'm not sure how this would be applied to word2vec, but it shouldn't be that hard.
class Translator:
    def __init__(self, model1, model2):


        self.model1 = model1
        self.model2 = model2

        self.vocab1 = self.model1.id2word
        self.vocab2 = self.model2.id2word

        self.vocabLength = len(self.vocab1)


        self.masterVocab = dict(self.vocab1)



        #Creates Master Dictionary to reference
        for key, value in self.vocab2.iteritems():
            if value in self.vocab1.itervalues():
                #self.masterVocab[key] = (key,value)
                self.masterVocab[key] = value
            elif value not in self.vocab1.itervalues():
                self.masterVocab[self.vocabLength] = value
                self.vocabLength += 1


    def topicsTranslate(self, topic1, topic2):

        expandedVocab1 = []
        expandedVocab2 = []

        ldaVec1 = sorted(self.model1.get_topic_terms(topic1, topn=self.model1.num_terms))
        ldaVec2 = sorted(self.model2.get_topic_terms(topic2, topn=self.model2.num_terms))

        added = True

        for key, value in self.masterVocab.iteritems():
            if value in self.vocab1.itervalues():
                expandedVocab1.append((key, ldaVec1[key][1]))
            else:
                expandedVocab1.append((key, 0))

            for key1,value1 in self.vocab2.iteritems():
                if value1 == value:
                    expandedVocab2.append((key, ldaVec2[key1][1]))
                    added = True
                    break
                added = False

            if added == False:
                expandedVocab2.append((key,0))

        return self.topicCompare(expandedVocab1, expandedVocab2, "Constant")


    def mostCommonTopics(self, model, topic):
        topicArray = []

        if model == "Model1":
            for x in range(0,50):
                print "Topic %d" % x
                rank = self.topicsTranslate(topic,x)

                struct = (rank, x, self.model2.show_topic(x), self.model1.show_topic(topic))


                topicArray.append(struct)

        if model == "Model2":
            for x in range(0,50):
                print "Topic %d" % x
                rank = self.topicsTranslate(topic,x)

                struct = (rank, x, self.model1.show_topic(x), self.model2.show_topic(topic))


                topicArray.append(struct)

        topicArray = sorted(topicArray, key=itemgetter(0), reverse=True)
        return topicArray


    def topicReturn(self,model,topic):
        return

    def topicCompare(self, top1, top2, key):
        #ldaVec1All = sorted(self.model1.get_topic_terms(top1, topn=self.model1.num_terms))
        #ldaVec2All = sorted(self.model2.get_topic_terms(top2, topn=self.model2.num_terms))

        ldaVec1Expand = []




        densePrune1 = self.vectorPrune(top1,self.model1,key)
        densePrune2 = self.vectorPrune(top2,self.model2,key)

        sim = np.sqrt(0.5 * ((np.sqrt(densePrune1) - np.sqrt(densePrune2))**2).sum())
        return sim

    def vectorPrune(self,vector,model,key):
        if key == "Constant":
            return self.vectorPruneConst(vector,model)
        elif key == "Dynamic":
            return self.vectorPruneDynamic(vector,model)

    #Sorts it by ID as well
    def vectorPruneConst(self, sparseVector,model):
        idSort = sparseVector
        valueSort = sorted(sparseVector, key=itemgetter(1), reverse=True)

        #valueSort = valueSort[:20]
        valueSort = [item[0] for item in valueSort[:15]]


        dense = gensim.matutils.sparse2full(idSort, self.vocabLength)

        for x in range (0, dense.__len__()):
            if x not in valueSort:
                dense[x] = 0

        return dense

        #for element in idSort


    #Tries to find the floor of when the words in a topic start to become insignificant. Needs development
    def vectorPruneDynamic(self, sparseVector, model):
        idSort = sparseVector
        valueSort = sorted(sparseVector, key=itemgetter(1), reverse=True)


        differenceCount = 0
        value1 = valueSort[0][1]
        value1 = math.floor(value1 * (10 ** 7)) / (10 ** 7)

        topWords = [valueSort[0][0]]

        for item in valueSort[1:]:
            value2 = item[1]
            value2 = math.floor(value2 * (10 ** 7)) / (10 ** 7)

            difference = value1 - value2

            #difference = long(long(difference * 1000)) / (1000))
            #if difference != 0:
            #    break
            if difference == 0:
                differenceCount +=1
                topWords.append(item[0])
                if differenceCount == 5:
                    break
            else:
                differenceCount = 0
                topWords.append(item[0])

            value1 = value2

        dense = gensim.matutils.sparse2full(idSort, self.vocabLength)

        i = 0
        for element in dense:
            if i not in topWords:
                element = 0
            i+=1

        for x in range (0, dense.__len__()):
            if x not in topWords:
                dense[x] = 0

        return dense


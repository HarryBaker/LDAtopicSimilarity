__author__ = 'Harry Baker'

import gensim
import numpy as np
import sympy
from operator import itemgetter
from gensim import matutils
import math

from math import log10, floor
from topic2vec import topic2vec

#credit to http://stackoverflow.com/questions/3410976/how-to-round-a-number-to-significant-figures-in-python
#def round_sig(x, sig=4):
#    return round(x, sig-int(floor(log10(x)))-1)


#topic similarity taies an LDA model, a list of sentances that were saved concurrently, and a flag of whether this model
#has been created and saved before. If the flag is to not load, it loads the model saved at filename. Otherwise, it saves
#a word2vec model at filename. There might be a more elegent way to handle that

#This class finds the similarity of all topics within a model
class TopicSimilarity():
    def __init__(self, LDA,sentances, flag, filename):
        print "Topic Similarity!"
        self.model = LDA
        #self.topics = LDA.num_topics

        self.topics = []
        for x in range(0,50):
            topic = self.model.show_topic(x)
            self.topics.append(topic)

        #The actual topic2vec object
        self.topic2vec = topic2vec(sentances,self.model, flag = flag, filename= filename,  size=600,window=5,mincount=10)
        #self.LDA2Vec2 = self.ldaTop2Vec("word2vec")


        #These are the results of the similarity of each topic to each other topic, saved as a 2D matrix

        self.cosine = self.cossineSim()
        self.LDAhessingerSparse = self.HessingerDistanceSparse()
        self.LDAhessingerDense = self.HessingerDistancePrune("Constant")
        self.topic2vecSimMat = self.topic2vecSim()
        self.topic2vecSimMatTop10 = self.topic2vecSimTop10()
        self.LDA2Vec = self.ldaTop2Vec("topic2vec")


        print "sim suite done"


    #topics from 0 to 49
    #Works by grabbing the given topic ID from the master matrix
    def findSimilarity(self, topicID):
        #lda2v1 = self.LDA2Vec1[topicID][10:]
        #lda2v1 = self.LDA2Vec[topicID][10:]
        top = self.topics[topicID][1:10]
        cos = self.cosine[topicID][1:10]
        hesSpar = self.LDAhessingerSparse[topicID][1:10]
        hesDen = self.LDAhessingerDense[topicID][1:10]
        t2v = self.topic2vecSimMat[topicID][1:10:]
        t2vW = self.topic2vecSimMatTop10[topicID][1:10:]

        #lda2v2 = self.LDA2Vec2[topicID]

        output = [("cos", cos), ("hesDen", hesDen), ("t2v", t2v), ("t2v", t2vW)]
        return output
        print "sim found"


    #Does topic2vec similarity rankings for the topic2vec model and the plain word2vec model.
    def ldaTop2Vec(self, key):
        print "lda topic2vec"
        simMatrixCos = []

        for x in range(0,50):
            topicMatrixCos = []
            for y in range(0,50):
                model = self.model

                #vec1 = model.get_topic_terms(x, topn=model.num_terms)


                #ldaVec1 = sorted(model.get_topic_terms(x, topn=model.num_terms))
                #ldaVec2 = sorted(model.get_topic_terms(y, topn=model.num_terms))

                ldaVec1 = model.show_topic(x, topn = 15)
                ldaVec2 = model.show_topic(y, topn = 15)

                lda1 = [tuple[0] for tuple in ldaVec1]
                lda2 = [tuple[0] for tuple in ldaVec2]


                if key == "topic2vec":
                    lda1 = [tuple[0] for tuple in ldaVec1 if tuple[0] in self.topic2vec.topic2vec.vocab]
                    lda2 = [tuple[0] for tuple in ldaVec2 if tuple[0] in self.topic2vec.topic2vec.vocab]
                    sim = self.topic2vec.topic2vec.n_similarity(lda1, lda2)
                elif key == "word2vec":
                    lda1 = [tuple[0] for tuple in ldaVec1 if tuple[0] in self.topic2vec.word2vec.vocab]
                    lda2 = [tuple[0] for tuple in ldaVec2 if tuple[0] in self.topic2vec.word2vec.vocab]
                    sim = self.topic2vec.word2vec.n_similarity(lda1, lda2)
                #simDict = (x, y, sim, self.model.show_topic(y))
                simDict = (x, y, sim)



                topicMatrixCos.append(simDict)

            simMatrixCos.append(sorted(topicMatrixCos, key=itemgetter(2), reverse=True))

        #for element in simMatrix:
        #    print simMatrix
        #topic1Sorted = sorted(simMatrixCos[0], key=itemgetter(2))
        #x = topic1Sorted
        return simMatrixCos

    #does a similarity query of the words that are most similar to each topic. For example, if the top 5 words associeted
    #with u'5' are ["apple", "pear", "dirt", "tree", "bug"], and u'7' are ["watermelon", "ant", "dirt", "tree", "bug"],
    #then this function would compare the similarity of the two lists.
    def topic2vecSimTop10(self, N):
        print "topic2vec sim top N words"
        simMatrixTop10 = []
        for x in range(0,50):
            topicMatrixTop = []

            for y in range(0,50):

                xWords = self.topic2vec.topic2vec.most_similar(positive=["u" + str(x)], topn=N)
                yWords = self.topic2vec.topic2vec.most_similar(positive=["u" + str(y)], topn=N)

                xWords2 = [pair[0] for pair in xWords]
                yWords2 =[pair[0] for pair in yWords]


                sim = self.topic2vec.topic2vec.n_similarity(xWords2, yWords2)
                #topicMatrixTop.append((x, y, sim, self.model.show_topic(y)))
                topicMatrixTop.append((x, y, sim))
            simMatrixTop10.append(sorted(topicMatrixTop, key=itemgetter(2), reverse=True))

        return simMatrixTop10

    #Compares the similarity of the topic tokens. Ie, directly comparing the token "topic5" (in this5 case u'5') to topic7
    #to guage similarity
    def topic2vecSim(self):
        print "token to token sim"
        simMatrixTop = []
        for x in range(0,50):
            topicMatrixTop = []

            for y in range(0,50):

                sim = self.topic2vec.topic2vec.similarity('u' + str(x), 'u' + str(y))
                #topicMatrixTop.append((x, y, sim, self.model.show_topic(y)))
                topicMatrixTop.append((x, y, sim))

            simMatrixTop.append(sorted(topicMatrixTop, key=itemgetter(2), reverse=True))

        return simMatrixTop



    #cossine similarity of the top N words in each topic
    def cossineSim(self, N):
        print "Cossine sim"
        simMatrixCos = []

        for x in range(0,50):
            topicMatrixCos = []
            for y in range(0,50):
                model = self.model

                vec1 = model.get_topic_terms(x, topn=model.num_terms)


                #ldaVec1 = sorted(model.get_topic_terms(x, topn=model.num_terms))
                #ldaVec2 = sorted(model.get_topic_terms(y, topn=model.num_terms))

                ldaVec1 = model.get_topic_terms(x, topn = N)
                ldaVec2 = model.get_topic_terms(y, topn = N)

                #dense1 = gensim.matutils.sparse2full(ldaVec1, model.num_terms)
                #dense2 = gensim.matutils.sparse2full(ldaVec2, model.num_terms)

                sim = matutils.cossim(ldaVec1, ldaVec2)
                #simDict = (x, y, sim, self.model.show_topic(y))
                simDict = (x, y, sim)



                topicMatrixCos.append(simDict)

            simMatrixCos.append(sorted(topicMatrixCos, key=itemgetter(2), reverse=True))

        #for element in simMatrix:
        #    print simMatrix
        #topic1Sorted = sorted(simMatrixCos[0], key=itemgetter(2))
        #x = topic1Sorted
        return simMatrixCos

    def HessingerDistance(self):
        return

    def HessingerDistancePrune(self, key):
        print "hessinger prune"
        simMatrixHes = []

        for x in range(0,50):
            print "Calculating Topic %d" % x
            topicMatrixHes = []

            for y in range(0,50):
                model = self.model

                vec1 = model.get_topic_terms(x, topn=model.num_terms)

                ldaVec1All = sorted(model.get_topic_terms(x, topn=model.num_terms))
                ldaVec2All = sorted(model.get_topic_terms(y, topn=model.num_terms))

                densePrune1 = self.vectorPrune(ldaVec1All,key)
                densePrune2 = self.vectorPrune(ldaVec2All,key)

                sim = np.sqrt(0.5 * ((np.sqrt(densePrune1) - np.sqrt(densePrune2))**2).sum())
                #simDict = (x, y, sim, self.model.show_topic(y), densePrune2)
                simDict = (x, y, sim)

                topicMatrixHes.append(simDict)

            simMatrixHes.append(sorted(topicMatrixHes, key=itemgetter(2)))


        return simMatrixHes

    def HessingerDistanceStandard(self,flag):
        print "Hessinger Standard"
        simMatrixHes = []

        for x in range(0,50):
            topicMatrixHes = []

            for y in range(0,50):
                model = self.model

                #ldaVec1All = sorted(model.get_topic_terms(x, topn=model.num_terms))
                #ldaVec2All = sorted(model.get_topic_terms(y, topn=model.num_terms))


                ldaVec1All = sorted(model.get_topic_terms(x, topn=40))
                ldaVec2All = sorted(model.get_topic_terms(y, topn=40))


                dense1Long = gensim.matutils.sparse2full(ldaVec1All, model.num_terms)
                dense2Long = gensim.matutils.sparse2full(ldaVec2All, model.num_terms)

                sim = np.sqrt(0.5 * ((np.sqrt(dense1Long) - np.sqrt(dense2Long))**2).sum())
                #simDict = (x, y, sim, self.model.show_topic(y))
                simDict = (x, y, sim)

                topicMatrixHes.append(simDict)


            simMatrixHes.append(sorted(topicMatrixHes, key=itemgetter(2)))

        #for element in simMatrix:
        #    print simMatrix
        #topic1Sorted = sorted(simMatrixHes[0], key=itemgetter(2))
        #x = topic1Sorted
        return (simMatrixHes)



    def HessingerDistanceSparse(self):
        print "Hessinger Sparse"
        simMatrixHes = []

        for x in range(0,50):
            topicMatrixHes = []

            for y in range(0,50):
                model = self.model


                ldaVec1All = sorted(model.get_topic_terms(x, topn=model.num_terms))
                ldaVec2All = sorted(model.get_topic_terms(y, topn=model.num_terms))

                sim = np.sqrt(0.5 * ((np.sqrt(ldaVec1All) - np.sqrt(ldaVec2All))**2).sum())
                #simDict = (x, y, sim, self.model.show_topic(y))
                simDict = (x, y, sim)

                topicMatrixHes.append(simDict)

            simMatrixHes.append(sorted(topicMatrixHes, key=itemgetter(2)))

        #for element in simMatrix:
        #    print simMatrix
        #topic1Sorted = sorted(simMatrixHes[0], key=itemgetter(2))
        #x = topic1Sorted
        return (simMatrixHes)

    def vectorPrune(self,vector,key):
        if key == "Constant":
            return self.vectorPruneConst(vector)
        elif key == "Dynamic":
            return self.vectorPruneDynamic(vector)

    #Sorts it by ID as well
    def vectorPruneConst(self, sparseVector):
        idSort = sparseVector
        valueSort = sorted(sparseVector, key=itemgetter(1), reverse=True)

        #valueSort = valueSort[:20]
        valueSort = [item[0] for item in valueSort[:20]]







        #valueSort = valueSort.reverse

        #differenceCount = 0
        #value1 = valueSort[0][1]
        #value1 = math.floor(value1 * (10 ** 7)) / (10 ** 7)

        #topWords = [valueSort[0][0]]

        #for item in valueSort[1:]:
        #    value2 = item[1]
        #    value2 = math.floor(value2 * (10 ** 7)) / (10 ** 7)

        #    difference = value1 - value2

            #difference = (long(difference * 1000)) / (1000)
            #if difference != 0:
            #    print "break"
         #   if difference == 0:
         #       differenceCount +=1
         #       topWords.append(item[0])
         #       if differenceCount == 5:
         #           break
         #   else:
         #       differenceCount = 0
         #       topWords.append(item[0])

          #  value1 = value2

        dense = gensim.matutils.sparse2full(idSort, self.model.num_terms)

        #i = 0
        #for element in dense:
        #    if i not in topWords:
        #        element = 0
        #    i+=1

        #for x in range (0, dense.__len__()):
        #    if x not in topWords:
        #        dense[x] = 0

        for x in range (0, dense.__len__()):
            if x not in valueSort:
                dense[x] = 0

        return dense

        #for element in idSort

    def vectorPruneDynamic(self, sparseVector):
        idSort = sparseVector
        valueSort = sorted(sparseVector, key=itemgetter(1), reverse=True)






        #valueSort = valueSort.reverse

        differenceCount = 0
        value1 = valueSort[0][1]
        value1 = math.floor(value1 * (10 ** 7)) / (10 ** 7)

        topWords = [valueSort[0][0]]

        for item in valueSort[1:]:
            value2 = item[1]
            value2 = math.floor(value2 * (10 ** 7)) / (10 ** 7)

            difference = value1 - value2

            difference = (long(difference * 1000)) / (1000)
            if difference != 0:
                print "break"
            if difference == 0:
                differenceCount +=1
                topWords.append(item[0])
                if differenceCount == 5:
                    break
            else:
                differenceCount = 0
                topWords.append(item[0])

            value1 = value2

        dense = gensim.matutils.sparse2full(idSort, self.model.num_terms)

        i = 0
        for element in dense:
            if i not in topWords:
                element = 0
            i+=1

        for x in range (0, dense.__len__()):
            if x not in topWords:
                dense[x] = 0

        return dense



    def sortTopic(self, matrix, topic):
        sortedTopic = sorted(matrix[topic], key=itemgetter(2))
        return sortedTopic

    def showTopicWord(self, matrix, topic):
        words = self.model.show_topic(topic)
        return words

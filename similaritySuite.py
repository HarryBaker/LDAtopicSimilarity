__author__ = 'loaner'
from topic2vec import topic2vec
from LDATopicSimilarity import TopicSimilarity
import sys
import cmd

#Should probably do something with inheritance.
#need to do better error handling
class similaritySuite(cmd.Cmd):
    def __init__(self, topic2vecSimilarity):

        cmd.Cmd.__init__(self)

        self.simSuite = topic2vecSimilarity
        self.topic2vec = self.simSuite.topic2vec
        self.LDAmodel = self.simSuite.model


        self.topics = self.topic2vec.ldaTopics
        self.topic2vecTopics = self.topic2vec.topicVecs

        print "Topic2vec Testing Suite"
        print "Commands are: "
        print "printTopic [topicID] ~~ if no topicID is given, will print all"
        print "mostSimilar [topicID]"



        #while (1):
        #   print "Enter Input"
        #    print "Options: most similar [topic]"


    def do_printTopic(self,topicID=None):

        if topicID:
            print
            print topicID
            print self.topics[int(topicID)]
            print
        else:
            i = 0
            for topic in self.topics:
                print
                print i
                print topic
                print
                i+=1


    #how to do output?
    def do_mostSimilar(self, topic):

        acceptable = []
        for y in range(0,50):
            acceptable.append(y)

        if int(topic) in acceptable:
            output = self.simSuite.findSimilarity(int(topic))


            #for x in range (0,10):
            #    output[0][1][0][x] = str(output[0][1][0][x])

            #there's gotta be a better way to do this
            #turn the output into a data structure/class
            print output[0][0] + " | " + output[1][0] + " | " + output[2][0] + " | " + output[3][0]
            print "----------------------------------"
            #print "%d    |      %d     |  %d  | %d" %(output[0][1][0][1] + "   | " + output[1][1][0][1], output[2][1][0][1], output[3][1][0][1]
            print "%d  |   %d  |  %d  | %d" % (output[0][1][0][1], output[1][1][0][1], output[2][1][0][1], output[3][1][0][1])
            print "%d  |   %d  |  %d  | %d" % (output[0][1][1][1], output[1][1][1][1], output[2][1][1][1], output[3][1][1][1])
            print "%d  |   %d  |  %d  | %d" % (output[0][1][2][1], output[1][1][2][1], output[2][1][2][1], output[3][1][2][1])
            print "%d  |   %d  |  %d  | %d" % (output[0][1][3][1], output[1][1][3][1], output[2][1][3][1], output[3][1][3][1])
            print "%d  |   %d  |  %d  | %d" % (output[0][1][4][1], output[1][1][4][1], output[2][1][4][1], output[3][1][4][1])
            print "%d  |   %d  |  %d  | %d" % (output[0][1][5][1], output[1][1][5][1], output[2][1][5][1], output[3][1][5][1])
            print "%d  |   %d  |  %d  | %d" % (output[0][1][6][1], output[1][1][6][1], output[2][1][6][1], output[3][1][6][1])
            print "%d  |   %d  |  %d  | %d" % (output[0][1][7][1], output[1][1][7][1], output[2][1][7][1], output[3][1][7][1])
            print "%d  |   %d  |  %d  | %d" % (output[0][1][8][1], output[1][1][8][1], output[2][1][8][1], output[3][1][8][1])
            print "%d  |   %d  |  %d  | %d" % (output[0][1][9][1], output[1][1][9][1], output[2][1][9][1], output[3][1][9][1])
        else:
            print "Please Chose Acceptable Topic ID"





        print "Enter new command"



#if __name__ == "__main__":
#    x = similaritySuite
#    x.cmdloop




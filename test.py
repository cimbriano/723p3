from model1 import *
import model1
import wsd
import util
import wsddata

ttable = model1.uniformTTableInitialization(simpleTestCorpus)

#temp = model1.alignSentencePair(ttable, simpleTestCorpus[0][0], simpleTestCorpus[0][1])                                                                       

corpus = readCorpus('Science.en', 'Science.fr', truncateWordLength=5)

ttable = runEM(corpus)

printTTable(ttable, 'ttable.out')

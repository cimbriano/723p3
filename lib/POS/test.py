from parser import *
from util import *
from tree import *
from grammar import *
from sys import *
from extractGrammar import *
import thread

def main(args):

	which_part = args[1] if len(args) == 2 else None

	if which_part == "1":  			partI()
	elif which_part == "2": 		partII()
	elif which_part == "3": 		partIII()
	elif which_part == "all":		all_parts()
	elif which_part == "train":		train()
	elif which_part == "test":		test()
	elif which_part == "experiment":experiment()
	else: 							usage()
		

def partI():
	print "Part I: Unary Rules"
	print str(timeFliesPCFG)
	print timeFliesSent
	print parse(timeFliesPCFG, timeFliesSent) # produced None , which is wrong

def partII():
	print "Part II: Warming up with Time Flies"
	myTree = parse(timeFliesPCFG2, timeFliesSent)
	print "myTree: "
	print myTree
	print "desiredTimeFliesParse: "
	print desiredTimeFliesParse
	print evaluate(desiredTimeFliesParse, myTree)

def partIII():
	print "Part III: Parsing English"

	#filename = 'wsj.dev'
	#print "Data file: " + filename
	#pcfg = computePCFG(filename)
	#print "PCFG length: " + str(len(pcfg))
	#print str(pcfg)
	# print "wsj.train"
	# pcfg = computePCFG('wsj.dev')
	# print "length: " + str(len(pcfg))
	# print parse(pcfg, ['NN', 'VBZ', 'IN', 'DT', 'NN']) 
	# print parse(pcfg, ['VBZ', 'NN', 'IN', 'DT', 'NN'])

	print
	print nonBinaryTree

	#print "Default binarization"
	#print binarizeTree(nonBinaryTree)

	print "annotation"
	tree = binarizeTree(nonBinaryTree, verticSize=4)
	print tree
	print 
#
#	print "Binarization with horizSize equals 2"
#	print binarizeTree(nonBinaryTree, horizSize=2)
#	
#
#	print "Annotate Children Test: vertical  = 2 (parent annotation only"
#	print binarizeTree(nonBinaryTree, verticSize=2)
	
	
	#print "Both horiz and vertical = 2"
	#print binarizeTree(nonBinaryTree, verticSize=2, horizSize=2)

	#print evaluateParser(pcfg, 'wsj.dev')

def train():
	print "training on wsj.train"
	print "Computing PCFG"
	pcfg = computePCFG('wsj.train', horizSize=2, verticSize=3)
	
	print "Evaluating Parser with pruning percent 0.001"
	print evaluateParser(pcfg, 'wsj.dev', pruningPercent=0.001)
	
def test():
	print "Computing PCFG"
	pcfg = computePCFG('wsj.train', horizSize=2, verticSize=2)
	print "Running parser on test"
	runParserOnTest(pcfg, 'wsj.test', 'wsj.test.out', pruningPercent=0.00001)

def experiment():

	# max_score = 0
	# best_hsize = 0
	# best_vsize = 0
	prune = 0.00001
	h_range = range(1,3)
	v_range = range(2,4)

	out_filename = "experiment.out.h" + str(h_range[0]) + "-" + str(h_range[-1]) \
	+ ".v" + str(v_range[0]) + "-" + str(v_range[-1]) + ".p" + str(prune) + ".txt"

	out = open("experiment/" + out_filename, 'w')
	out.write("h\t\tv\t\tprune\t\tscore\n")

	for hsize in h_range:
		for vsize in v_range:
			print "Running: hsize = " + str(hsize) + ", vsize = " + str(vsize)

			pcfg = computePCFG('wsj.train', horizSize=hsize, verticSize=vsize)
			score = evaluateParser(pcfg, 'wsj.dev', pruningPercent=prune)

			out.write(str(hsize) + "\t\t" + str(vsize) + "\t\t" + str(prune) + "\t\t" + str(score) + "\n")



def all_parts():
	partI()
	partII()
	partIII()

def usage():
	print "Bad argument"
	print "Include 1 2 3 or all"
	print "usage: test.py [ 1 | 2 | 3 ]"

if __name__ == '__main__':
	main(sys.argv)
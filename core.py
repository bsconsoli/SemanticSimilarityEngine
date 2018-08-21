import sys, os, traceback
import argparse
import ms_annotator as msa
import numpy as np


#Interpret corpus and send a X (number of pairs) by 3 (similarity, head and tail) matrix to annotator module
def send_to_ms_annotator(corpus, parser):

	with open(corpus) as f:
		lines = [line.rstrip('\n') for line in f]

	pp_corpus = []
	for l in lines:
		if "<pair" in l:
			similarity = l[(l.find('similarity="')+12):(l.find('"', l.find('similarity="')+12))]
		if "<t>" in l:
			s1 = l[l.find("<t>")+3:l.find("/<t>")-3]
		if "<h>" in l:
			s2 = l[l.find("<h>")+3:l.find("/<h>")-3]
		if "</pair>" in l:
			pair = [similarity, s1, s2]
			pp_corpus.append(pair)
	pp_corpus = np.array(pp_corpus)

	return msa.get_ms_info(pp_corpus, parser)


def calculate_morphosyntactic_features(tokenized_corpus):
	#TODO: Send tokenized corpus to MS feature calculation module
	print('ello')

parser = argparse.ArgumentParser(description="Some semantic similarity measurement system.")
parser.add_argument("-msp", "--morphosyntaxparser", choices=["maltparser", "visl"], help="Determine morphosyntax parser will be used.")
parser.add_argument("-c", "--corpus", help="File of the corpus whose similarity will be calculated.")
parser.add_argument("-msfc", "--morphosyntacticfeaturecalculation", help="Morphosyntactic feature calculation. Provide tokenized corpus as argument.")
#parser.add_argument("-ac", "--annotatedcorpus", help="File of the tokenized corpus for morphosyntactic feature calculation.")

args = parser.parse_args()

#Annotation
if args.corpus and args.morphosyntaxparser:
	annotated_corpus = send_to_ms_annotator(args.corpus, args.morphosyntaxparser)
	ac = open("corpus_anotado.txt", "w+")
	for i in range(annotated_corpus.shape[0]):
		#Annotation Into File Formatting
		ac.write("<pair>\n<sr>\n" + annotated_corpus[i,0] + "\n<\sr>\n")
		ac.write("\n<s1>\n" + annotated_corpus[i,1]+"<\s1>\n")
		ac.write("<s2>\n" + annotated_corpus[i,2]+"<\s2>\n<\pair>\n\n")
	ac.close()
elif args.corpus ^ args.morphosyntaxparser:
	print("Must provide morphosyntax parser option when providing corpus and vice versa.")
	sys.exit(1)

#morphosyntactic feature calculation
if args.morphosyntacticfeaturecalculation:
	calculate_morphosyntactic_features(args.morphosyntacticfeaturecalculation)

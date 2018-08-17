import sys, os, traceback
import argparse
import tokenizer
import numpy as np

def send_to_tokenizer(corpus, parser):
	#TODO: Interpret corpus and send a X (number of pairs) by 3 (similarity, head and tail) matrix to tokenizer
	#The function returns the name of the file created by the tokenizer.
	with open(corpus) as f:
		lines = [line.rstrip('\n') for line in f] for line in f
	pp_corpus = np.array()
	for l in lines:
		similarity = l[l.find('"')+1, l.find('"', l.find('"'))]
		s1 = l[l.find("<t>")+3, l.find("\\<t>")]
		s2 = l[l.find("<h>")+3, l.find("\\<h>")]
		pair = [similarity, s1, s2]
		pp_corpus = np.append(pp_corpus, [pair])
	#TOKENIZER WILL WORK WITH pp_corpus MATRIX


def calculate_morphosyntactic_features(tokenized_corpus):
	#TODO: Send tokenized corpus to MS feature calculation module

parser = argparse.ArgumentParser(description="Some semantic similarity measurement system.")
parser.add_argument("-msp", "--morphosyntaxparser", choices=["maltparser", "visl"], help="Determine morphosyntax parser will be used.")
parser.add_argument("-c", "--corpus", help="File of the corpus whose similarity will be calculated.")
parser.add_argument("-msfc", "--morphosyntacticfeaturecalculation", help="Morphosyntactic feature calculation. Provide tokenized corpus as argument.")
#parser.add_argument("-tc", "--tokenizedcorpus", help="File of the tokenized corpus for morphosyntactic feature calculation.")

args = parser.parse_args()

#tokenization
if args.corpus and args.morphsyntaxparser:
	tokenized_corpus = send_to_tokenizer(args.corpus, args.morphosyntaxparser)
elif args.corpus ^ args.morphsyntaxparser:
	print("Must provide morphosyntax parser option when providing corpus and vice versa.")
	sys.exit(1)

#morphosyntactic feature calculation
if args.morphosyntacticfeaturecalculation:
	calculate_morphosyntactic_features(args.morphosyntacticfeaturecalculation)

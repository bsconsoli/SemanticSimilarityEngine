import sys, os, traceback
import argparse
import ms_annotator as msa
import ms_calculator as msc
import s_calculator as sc
import ml_module as mlc
import numpy as np


#Interpret corpus and send a X (number of pairs) by 3 (similarity, head and tail) matrix to annotator module
def send_to_ms_annotator(corpus, parser):

	with open(corpus) as f:
		lines = [line.rstrip('\n') for line in f]

	pp_corpus = []
	for l in lines:
		if "<pair" in l:
			similarity = l[(l.find('similarity="')+12):(l.find('"', l.find('similarity="')+12))]
			id_pair = l[(l.find('id="')+4):(l.find('"', l.find('id="')+4))]
		if "<t>" in l:
			s1 = l[l.find("<t>")+3:l.find("/<t>")-3]
		if "<h>" in l:
			s2 = l[l.find("<h>")+3:l.find("/<h>")-3]
		if "</pair>" in l:
			pair = [similarity, s1, s2, id_pair]
			pp_corpus.append(pair)
	pp_corpus = np.array(pp_corpus)

	return msa.get_ms_info(pp_corpus, parser)


#def calculate_morphosyntactic_features(tokenized_corpus):
	#TODO: Send tokenized corpus to MS feature calculation module
	

parser = argparse.ArgumentParser(description="Some semantic similarity measurement system.")
parser.add_argument("-msp", choices=["maltparser", "visl"], help="Determine morphosyntax parser will be used.")
parser.add_argument("-c", "--corpus", help="File of the corpus whose similarity will be calculated.")
parser.add_argument("-msfc", help="Morphosyntactic feature calculation. Provide annotated corpus as argument.")
#parser.add_argument("-msac", help="File of the tokenized corpus for morphosyntactic feature calculation.")
parser.add_argument("-sfc", help="Semantic feature calculation. Provide annotated corpus as argument.")
parser.add_argument("-trn", help="Training Data")


args = parser.parse_args()

#Annotation
if args.corpus: corp = True
else: corp = False
if args.msp: msparser = True
else: msparser = False

if corp and msparser:
	annotated_corpus = send_to_ms_annotator(args.corpus, args.msp)
	ac = open("corpus_anotado.txt", "w+")
	for i in range(annotated_corpus.shape[0]):
		#Annotation Into File Formatting
		ac.write("<pair>\n<id>"+ annotated_corpus[i,3] + "<\id>\n<sr>" + annotated_corpus[i,0] + "<\sr>\n")
		ac.write("<s1>\n" + annotated_corpus[i,1] + "\n<\s1>\n")
		ac.write("<s2>\n" + annotated_corpus[i,2] + "\n<\s2>\n<\pair>\n\n")
	ac.close()
elif corp ^ msparser:
	print("Must provide morphosyntax parser option when providing corpus for morphosyntactic annotation and vice versa.")
	sys.exit(1)

#morphosyntactic feature calculation
if args.msfc:
	pair_id_test, ms_feature_array_test = msc.calculate_ms_features(args.msfc)
	pair_id_train, ms_feature_array_train = msc.calculate_ms_features(args.trn)
	y_test = []
	y_train = []
	for ids in pair_id_test:
		y_test.append(float(ids[1]))
	y_test = np.array(y_test)
	for ids in pair_id_train:
		y_train.append(float(ids[1]))
	y_train = np.array(y_train)
	mlc.random_forests(ms_feature_array_test, y_test, ms_feature_array_train, y_train)


if args.sfc:
	sc.calculate_semantic_features(args.sfc)
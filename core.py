import sys, os, traceback
import argparse
import ms_annotator as msa
import ms_calculator as msc
import s_calculator as sc
import ml_module as mlc
import numpy as np
import itertools as it
from scipy.stats import pearsonr
from sklearn.metrics import mean_squared_error


#EXTRACT SENTENCES FROM CORPUS AND SEND A X (NUMBER OF PAIRS) BY 3 (SIMILARITY, HEAD AND TAIL) MATRIX TO ANNOTATOR MODULE
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

#PARSE ARGUMENTS
parser = argparse.ArgumentParser(description="Semantic similarity measurement system.")
parser.add_argument("-msp", choices=["maltparser", "visl"], help="Determine which morphosyntax parser will be used.")
parser.add_argument("-c", "--corpus", help="Corpus in the ASSIN 2016 format")
parser.add_argument("-tst", help="Annotaded Test Data")
parser.add_argument("-trn", help="Annotated Training Data")
parser.add_argument("-w2v", help="word2vec model to be used for feature calculation")

args = parser.parse_args()

#ANNOTATION RELATED ARGUMENTS
if args.corpus: corp = True
else: corp = False
if args.msp: msparser = True
else: msparser = False

#ANNOTATION
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
	print("Must provide morphosyntax parser option when providing corpus for morphosyntactic annotation and vice versa.\n")
	sys.exit(1)

#TRAIN/TEST RELATED ARGUMENTS
if args.trn: train = True
else: train = False
if args.tst: test = True
else: test = False
if args.w2v: word2vec = True
else: word2vec = False

#TRAIN MODEL WITH TRN AND TEST IT WITH TST
if test and train and word2vec:

	we_model = sc.wordembeddings_load(args.w2v)
	
	feature_names = ['wtotal', 's1%', 's2%', 'we']

	pair_id_test, feature_array_test = msc.calculate_ms_features(args.tst)
	pair_id_train, feature_array_train = msc.calculate_ms_features(args.trn)

	s_feature_array_test = sc.calculate_semantic_features(args.tst, we_model)
	s_feature_array_train = sc.calculate_semantic_features(args.trn, we_model)

	for i in range(len(feature_array_test)):
		feature_array_test[i].extend(s_feature_array_test[i])

	for i in range(len(feature_array_train)):
		feature_array_train[i].extend(s_feature_array_train[i])

	y_test = []
	y_train = []
	for ids in pair_id_test:
		y_test.append(float(ids[1]))
	y_test = np.array(y_test)
	for ids in pair_id_train:
		y_train.append(float(ids[1]))
	y_train = np.array(y_train)

	Z_test, svr_results = mlc.svr(np.array(feature_array_test), y_test, np.array(feature_array_train), y_train)
	print( 'Pearson r: ', pearsonr(y_test, svr_results)[0], '\nMSE: ', mean_squared_error(y_test, svr_results))
elif (train ^ test) ^ word2vec:
	print("Must provide training corpus, test corpus and word2vec word embeddings model in order to test a semantic similarity model.\n")
	sys.exit(1)
import numpy as np
from collections import defaultdict
import gensim as gs
import os
import xml.etree.ElementTree as ET

#TAKES PAIR XML CODE AND PUTS INFORMATION INTO A MAT
def xml_to_matrix(pair_lines):
	reading_sentence_1 = False
	reading_sentence_2 = False
	tokens_1 = []
	tokens_2 = []
	for l in pair_lines:
		if l.find('<id>') != -1:
			pair_id = l.replace('<id>', '').replace('<\id>', '')
			continue
		if l.find('<sr>') != -1:
			pair_sr = l.replace('<sr>', '').replace('<\sr>', '')
			continue
		if l.find('<s1>') != -1:
			reading_sentence_1 = True
			continue
		if l.find('<s2>') != -1:
			reading_sentence_2 = True
			continue
		if l.find('<\s1>') != -1:
			reading_sentence_1 = False
			continue
		if l.find('<\s2>') != -1:
			reading_sentence_2 = False
			continue
		if reading_sentence_1:
			tokens_1.append(l.split('\t'))
			continue
		if reading_sentence_2:
			tokens_2.append(l.split('\t'))
			continue
	return [pair_id, pair_sr, np.array(tokens_1), np.array(tokens_2)]

#CALCULATES WORD EMBEDDINGS BASED FEATURE
def s_feature_calculator(s1, s2, we_model):
	we_word_score_average = 0
	we_word_scores = []

	for i in range(s1.shape[0]):
		best_we_word_score = 0
		if s1[i][3] == 'PU' or s1[i][3] == 'DET' or s1[i][3] == 'PRP' or s1[i][3] == 'KC' or s1[i][3] == '.' or s1[i][3] == 'CONJ' or s1[i][3] == 'ADP': continue
		for j in range(s2.shape[0]):
			word_sentence_1 = s1[i][1].lower()
			word_sentence_2 = s2[j][1].lower()
			if word_sentence_1 == word_sentence_2:
				best_we_word_score = 1
				best_word = word_sentence_2
			if word_sentence_1 in we_model.vocab and word_sentence_2 in we_model.vocab:
				we_similarity_word = we_model.similarity(word_sentence_1, word_sentence_2)
				if best_we_word_score < we_similarity_word:
					best_we_word_score = we_similarity_word
					best_word = word_sentence_2

		we_word_scores.append(best_we_word_score)

	we_word_score_average = np.average(we_word_scores)

	if np.isnan(we_word_score_average):
		we_word_score_average = 0

	return [we_word_score_average]

#LOAD WORD EMBEDDING MODEL INTO MEMORY
def wordembeddings_load(w2v_file):
	return gs.models.KeyedVectors.load_word2vec_format(w2v_file, unicode_errors='ignore')

#METHOD CALLED BY OTHER MODULES IN ORDER TO CALCULATE WE FEATURES
def calculate_semantic_features(annotated_corpus, we_model):
	with open(annotated_corpus) as f:
		lines = [l.strip('\n') for l in f.readlines()]
	reading_pair = False
	pair_lines = []
	pair_matrixes = []
	for l in lines:
		if l == "<pair>":
			reading_pair = True
			pair_lines = []
			continue
		if l == "<\pair>":
			reading_pair = False
			pair_matrixes.append(xml_to_matrix(pair_lines))
			continue
		if reading_pair:
			pair_lines.append(l)
			continue

	semantic_features = []
	for pm in pair_matrixes:
		semantic_features.append(s_feature_calculator(pm[2],pm[3], we_model))
	return semantic_features
import numpy as np
from collections import defaultdict
import gensim as gs
import os
import xml.etree.ElementTree as ET

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

def get_ConceptNet_evaluation(w1, w2, database):
	relations = []
	entry = database[w1]
	for e in entry:
		if w2 == e[1]:
			relations.append([e[0], e[1], e[2]])
	return relations

def get_OntoPT_evaluation(w1, w2, database):
	synonym = False
	entry = database[w1]
	for e in entry:
		if w2 == e:
			synonym = True
			break
	return synonym

def s_feature_calculator(s1, s2, conceptnet_database, we_model, ontopt_database):
	#TEXT FILES RECORDINGS RESULTS OF EACH METHOD
	if os.path.exists('conceptnet_similarity.txt'): file_option_cn = 'a+'
	else: file_option_cn = 'w+'
	if os.path.exists('we_similarity.txt'): file_option_we = 'a+'
	else: file_option_we = 'w+'
	if os.path.exists('ontopt_similarity.txt'): file_option_we = 'a+'
	else: file_option_we = 'w+'
	conceptnet_file = open('conceptnet_similarity.txt', file_option_cn)
	we_file = open('we_similarity.txt', file_option_we)
	ontopt_file = open('ontopt_similarity.txt', file_option_we)

	counter_on = 0
	counter_cn = 0
	conceptnet_relations_word = []
	conceptnet_relations_lemma = []
	for i in range(s1.shape[0]):
		if s1[i][3] == '.' or s1[i][3] == 'NUM' or s1[i][3] == 'DET' or s1[i][3] == 'CONJ' or s1[i][3] == 'ADP':
			continue
		for j in range(s2.shape[0]):
			word_sentence_1 = s1[i][1].lower()
			word_sentence_2 = s2[j][1].lower()
			lemma_sentence_1 = s1[i][2].lower()
			lemma_sentence_2 = s2[j][2].lower()
			#CONCEPTNET DB SEARCH
			conceptnet_result_word = get_ConceptNet_evaluation(word_sentence_1, word_sentence_2, conceptnet_database)
			conceptnet_result_lemma = get_ConceptNet_evaluation(lemma_sentence_1, lemma_sentence_2, conceptnet_database)
			if conceptnet_result_word:
				conceptnet_relations_word.append(conceptnet_result_word)
				counter_cn += len(conceptnet_result_word)
			if conceptnet_result_lemma:
				conceptnet_relations_lemma.append(conceptnet_result_lemma)
				counter_cn += len(conceptnet_result_lemma)
			#WORDEMBEDDING DB SEARCH
			if word_sentence_1 in we_model.vocab and word_sentence_2 in we_model.vocab:
				we_similarity_word = we_model.similarity(word_sentence_1, word_sentence_2)
				if we_similarity_word > 0.7 and we_similarity_word < 0.99999:
					line_to_write = "Word[1]: " + word_sentence_1 + " | Word[2]: " + word_sentence_2 + " | Cosine Distance: " + str(we_similarity_word) + "\n\n"
					we_file.write(line_to_write)
			if lemma_sentence_1 in we_model.vocab and lemma_sentence_2 in we_model.vocab:
				we_similarity_lemma = we_model.similarity(lemma_sentence_1, lemma_sentence_2)
				#if we_similarity_lemma > 0.7 and we_similarity_lemma < 0.99999:
				line_to_write = "Lemma[1]: " + lemma_sentence_1 + " | Lemma[2]: " + lemma_sentence_2 + " | Cosine Distance: " + str(we_similarity_lemma) + "\n\n"
				we_file.write(line_to_write)
			#ONTOPT DB SEARCH
			ontopt_result_word = get_OntoPT_evaluation(word_sentence_1, word_sentence_2, ontopt_database)
			ontopt_result_lemma = get_OntoPT_evaluation(lemma_sentence_1, lemma_sentence_2, ontopt_database)
			if ontopt_result_word:
				line_to_write = word_sentence_1 + " is synomym of " + word_sentence_2 + '\n\n'
				ontopt_file.write(line_to_write)
				counter_on += 1
			if ontopt_result_lemma:
				line_to_write = lemma_sentence_1 + " is synomym of " + lemma_sentence_2 + '\n\n'
				ontopt_file.write(line_to_write)
				counter_on += 1

	if counter_cn > 0:
		line_to_write = "NUM RELAÇÕES: " + str(counter_cn) + "\nPALAVRA: | "
		for relations in conceptnet_relations_word:
			for relation in relations:
				line_to_write = line_to_write + relation[0] + " - " + relation[1] + " - " + relation[2] + " | "
		line_to_write = line_to_write + "\nLEMMA: | "
		for relations in conceptnet_relations_lemma:
			for relation in relations:
				line_to_write = line_to_write + relation[0] + " - " + relation[1] + " - " + relation[2] + " | "
		line_to_write = line_to_write + "\n\n"
		conceptnet_file.write(line_to_write)

	conceptnet_file.close()
	we_file.close()
	ontopt_file.close()


def calculate_semantic_features(annotated_corpus):
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
	#CONCEPTNET LOAD
	conceptnet_database = defaultdict(list)
	with open('semantic/conceptnet-assertions-pt.csv') as database:
		for line in database:
			head = line.split('\t')[2].split('/')[3]
			tail = line.split('\t')[3].split('/')[3]
			relation = line.split('\t')[1].split('/')[2]
			conceptnet_database[head].append([head, tail, relation])
	#WORDEMBEDDINGS LOAD
	we_model = gs.models.KeyedVectors.load_word2vec_format('semantic/NILC_cbow_s300.txt', unicode_errors='ignore')
	#ONTOPT LOAD
	ontopt_database = defaultdict(list)
	ontopt_xml = ET.parse('semantic/OntoPTv0.6.rdfs')
	rdf = ontopt_xml.getroot()
	for description in rdf:
		formas_lexicais = []
		for info in description:
			if info.tag.find('formaLexical') != -1:
				formas_lexicais.append(info.text)
		for i in range(len(formas_lexicais)):
			for j in range(len(formas_lexicais)):
				if i != j and formas_lexicais[j] not in ontopt_database[formas_lexicais[i]]:
					ontopt_database[formas_lexicais[i]].append(formas_lexicais[j])

	for pm in pair_matrixes:
		s_feature_calculator(pm[2],pm[3], conceptnet_database, we_model, ontopt_database)
	return pair_matrixes
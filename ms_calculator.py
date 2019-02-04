import numpy as np
import s_calculator as sc

#TAKES PAIR XML CODE AND PUTS INFORMATION INTO A MATRIX
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

#CALCULATES MORFOLOGICAL INFORMATION BASED FEATURES
def ms_feature_calculator(s1, s2):

	s1w1gram = 0
	s1l1gram = 0
	s1s1gram = 0
	s1wtotal = 0
	s1_size = s1.shape[0]

	s2w1gram = 0
	s2l1gram = 0
	s2s1gram = 0
	s2wtotal = 0
	s2_size = s2.shape[0]

	for i in range(s1.shape[0]):
		wyes = False
		lyes = False
		syes = False
		wtotalyes = False

		if s1[i][3] == 'PU' or s1[i][3] == 'DET' or s1[i][3] == 'PRP' or s1[i][3] == 'KC' or s1[i][3] == '.' or s1[i][3] == 'CONJ' or s1[i][3] == 'ADP': 
			s1_size -= 1

		for j in range(s2.shape[0]):
			if s1[i][3] == 'PU' or s1[i][3] == 'DET' or s1[i][3] == 'PRP' or s1[i][3] == 'KC' or s1[i][3] == '.' or s1[i][3] == 'CONJ' or s1[i][3] == 'ADP': continue
			if s1[i][1].lower() == s2[j][1].lower():
				if not wyes and not lyes and not wtotalyes and not syes:
					s1wtotal += 1
					wtotalyes = True
				if not wyes:
					points = 1
					s1w1gram += points
					wyes = True
			if s1[i][2].lower() == s2[j][2].lower():
				if not wyes and not lyes and not wtotalyes and not syes:
					s1wtotal += 1
					wtotalyes = True
				if not lyes:
					s1l1gram += 1
					lyes = True
			if s1[i][4].lower() == s2[j][4].lower():
				if not wyes and not lyes and not wtotalyes and not syes:
					s1wtotal += 1
					wtotalyes = True
				if not syes:
					s1s1gram += 1
					lyes = True

	for i in range(s2.shape[0]):
		wyes = False
		lyes = False
		syes = False
		wtotalyes = False

		if s2[i][3] == 'PU' or s2[i][3] == 'DET' or s2[i][3] == 'PRP' or s2[i][3] == 'KC' or s2[i][3] == '.' or s2[i][3] == 'CONJ' or s2[i][3] == 'ADP': 
			s2_size -= 1

		for j in range(s1.shape[0]):
			if s2[i][3] == 'PU' or s2[i][3] == 'DET' or s2[i][3] == 'PRP' or s2[i][3] == 'KC' or s2[i][3] == '.' or s2[i][3] == 'CONJ' or s2[i][3] == 'ADP': continue
			if s2[i][1].lower() == s1[j][1].lower():
				if not wyes and not lyes and not wtotalyes:
					s2wtotal += 1
					wtotalyes = True
				if not wyes:
					points = 1
					s2w1gram += points
					wyes = True
			if s2[i][2].lower() == s1[j][2].lower():
				if not wyes and not lyes and not wtotalyes:
					s2wtotal += 1
					wtotalyes = True
				if not lyes:
					s2l1gram += 1
					lyes = True
			if s2[i][4].lower() == s1[j][4].lower():
				if not wyes and not lyes and not wtotalyes and not syes:
					s2wtotal += 1
					wtotalyes = True
				if not syes:
					s2s1gram += 1
					lyes = True

	word_features = [s1wtotal, s1wtotal/s1_size, s2wtotal/s2_size]
	return word_features

#METHOD CALLED BY OTHER MODULES TO CALCULATE MORPHOLOGICAL FEATURES
def calculate_ms_features(corpus):
	word = pos = dependency = True
	with open(corpus) as f:
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
	pair_identification = []
	ms_features = []
	for pm in pair_matrixes:
		ms_features.append(ms_feature_calculator(pm[2],pm[3]))
		pair_identification.append([pm[0], pm[1]])
	return pair_identification, ms_features
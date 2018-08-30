import numpy as np

#Returns [ID, SR, SENT_1(ID - Word - Lemma - POS - POS - _ - Father Node ID - Dependency Type - _ - _), SENT_2(Matrix ConLL)]
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

def ms_feature_calculator(s1, s2, info_choice):
	word, pos, dependency = info_choice
	w1gram = w2gram = w3gram = 0
	p1gram = p2gram = p3gram = 0
	d1gram = d2gram = d3gram = 0
	for i in range(s1.shape[0]):
		for j in range(s2.shape[0]):
			if word:
				if s1[i][1].lower() == s2[j][1].lower():
					w1gram += 1
				if i+1 < s1.shape[0] and j+1 < s2.shape[0]:
					if s1[i][1].lower() == s2[j][1].lower() and s1[i+1][1].lower() == s2[j+1][1].lower():
						w2gram += 1
				if i+2 < s1.shape[0] and j+2 < s2.shape[0]:
					if s1[i][1].lower() == s2[j][1].lower() and s1[i+1][1].lower() == s2[j+1][1].lower() and s1[i+2][1].lower() == s2[j+2][1].lower():
						w3gram += 1
			if pos:
				if  s1[i][3].lower() == s2[j][3].lower():
					p1gram += 1
				if i+1 < s1.shape[0] and j+1 < s2.shape[0]:
					if s1[i][3].lower() == s2[j][3].lower() and s1[i+1][3].lower() == s2[j+1][3].lower():
						p2gram += 1
				if i+2 < s1.shape[0] and j+2 < s2.shape[0]:
					if s1[i][3].lower() == s2[j][3].lower() and s1[i+1][3].lower() == s2[j+1][3].lower() and s1[i+2][3].lower() == s2[j+2][3].lower():
						p3gram += 1
			if dependency:
				if s1[i][7] == s2[j][7]:
					d1gram += 1
				if int(s1[i][6]) > 0:
					if s1[i][7] == s2[j][7] and s1[int(s1[i][6])-1][7] == s2[int(s2[j][6])-1][7]:
						d2gram += 1
				if int(s1[i][6]) > 0 and int(s1[int(s1[i][6])-1][6])-1 > 0:
					if s1[i][7] == s2[j][7] and s1[int(s1[i][6])-1][7] == s2[int(s2[j][6])-1][7] and s1[int(s1[int(s1[i][6])-1][6])-1][7] == s2[int(s2[int(s1[j][6])-1][6])-1][7]:
						d3gram += 1

	return [[w1gram,w2gram,w3gram], [p1gram,p2gram,p3gram], [d1gram,d2gram,d3gram]]

#Takes corpus annotated by ms_annotator and return a list with each item containing information about one pair
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
	for pm in pair_matrixes:
		print(ms_feature_calculator(pm[2],pm[3],[word,pos,dependency]))
	return pair_matrixes
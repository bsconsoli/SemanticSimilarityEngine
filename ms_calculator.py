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

def ms_feature_calculator(s1, s2, info_choice, file):
	word, pos, dependency = info_choice
	w1gram = w2gram = w3gram = 0
	p1gram = p2gram = p3gram = 0
	d1gram = d2gram = d3gram = 0
	for i in range(s1.shape[0]):
		file.write(s1[i][1])
		if i+1 == s1.shape[0]:
			continue
		file.write(' ')
	file.write('\n')
	for i in range(s2.shape[0]):
		file.write(s2[i][1])
		if i+1 == s2.shape[0]:
			continue
		file.write(' ')
	file.write('\n')
	w1yes = False
	w2yes = False
	w3yes = False
	l1yes = False
	l2yes = False
	l3yes = False
	p1yes = False
	p2yes = False
	p3yes = False
	d1yes = False
	d2yes = False
	d3yes = False
	for i in range(s1.shape[0]):
		w1yes = False
		w2yes = False
		w3yes = False
		p1yes = False
		p2yes = False
		p3yes = False
		d1yes = False
		d2yes = False
		d3yes = False
		for j in range(s2.shape[0]):
			if word:
				if s1[i][3] == '.' or s1[i][3] == 'DET' or s1[i][3] == 'CONJ' or s1[i][3] == 'ADP':
					continue
				if s1[i][1].lower() == s2[j][1].lower():
					if not w1yes:
						w1gram += 1
						w1yes = True
				if s1[i][2].lower() == s2[j][2].lower():
					if not w1yes:
						w1gram += 1
						w1yes = True

				if s1[i+1][3] == '.' or s1[i+1][3] == 'DET' or s1[i+1][3] == 'CONJ' or s1[i+1][3] == 'ADP':
					continue
				if i+1 < s1.shape[0] and j+1 < s2.shape[0]:
					if s1[i][1].lower() == s2[j][1].lower() and s1[i+1][1].lower() == s2[j+1][1].lower():
						if not w2yes:
							w2gram += 1
							w2yes = True
				if i+1 < s1.shape[0] and j+1 < s2.shape[0]:
					if s1[i][2].lower() == s2[j][2].lower() and s1[i+1][2].lower() == s2[j+1][2].lower():
						if not w2yes:
							w2gram += 1
							w2yes = True

				if s1[i+2][3] == '.' or s1[i+2][3] == 'DET' or s1[i+2][3] == 'CONJ' or s1[i+2][3] == 'ADP':
					continue
				if i+2 < s1.shape[0] and j+2 < s2.shape[0]:
					if s1[i][1].lower() == s2[j][1].lower() and s1[i+1][1].lower() == s2[j+1][1].lower() and s1[i+2][1].lower() == s2[j+2][1].lower():
						if not w3yes:
							w3gram += 1
							w3yes = True
				if i+2 < s1.shape[0] and j+2 < s2.shape[0]:
					if s1[i][2].lower() == s2[j][2].lower() and s1[i+1][2].lower() == s2[j+1][2].lower() and s1[i+2][2].lower() == s2[j+2][2].lower():
						if not w3yes:
							w3gram += 1
							w3yes = True

			if pos:
				if  s1[i][3].lower() == s2[j][3].lower():
					if not p1yes:
						p1gram += 1
						p1yes = True
				if i+1 < s1.shape[0] and j+1 < s2.shape[0]:
					if s1[i][3].lower() == s2[j][3].lower() and s1[i+1][3].lower() == s2[j+1][3].lower():
						if not p2yes:
							p2gram += 1
							p2yes = True
				if i+2 < s1.shape[0] and j+2 < s2.shape[0]:
					if s1[i][3].lower() == s2[j][3].lower() and s1[i+1][3].lower() == s2[j+1][3].lower() and s1[i+2][3].lower() == s2[j+2][3].lower():
						if not p1yes:
							p3gram += 1
							p3yes = True
			if dependency:
				if s1[i][7] == s2[j][7]:
					if not d1yes:
						d1gram += 1
						d1yes = True
				if int(s1[i][6]) > 0:
					if s1[i][7] == s2[j][7] and s1[int(s1[i][6])-1][7] == s2[int(s2[j][6])-1][7]:
						if not d2yes:
							d2gram += 1
							d2yes = True
				if int(s1[i][6]) > 0 and int(s1[int(s1[i][6])-1][6])-1 > 0:
					if s1[i][7] == s2[j][7] and s1[int(s1[i][6])-1][7] == s2[int(s2[j][6])-1][7] and s1[int(s1[int(s1[i][6])-1][6])-1][7] == s2[int(s2[int(s2[j][6])-1][6])-1][7]:
						if not d3yes:
							d3gram += 1
							d3yes = True
							file.write('S1 -- WORDS: ' + s1[i][1] + ' - ' + s1[int(s1[i][6])-1][1] + ' - ' + s1[int(s1[int(s1[i][6])-1][6])-1][1] + ' | Dependency: ' + s1[i][7] + ' - ' + s1[int(s1[i][6])-1][7] + ' - ' + s1[int(s1[int(s1[i][6])-1][6])-1][7] + '\n')
							file.write('S2 -- WORDS: ' + s2[j][1] + ' - ' + s2[int(s2[j][6])-1][1] + ' - ' + s2[int(s2[int(s2[j][6])-1][6])-1][1] + ' | Dependency: ' + s2[j][7] + ' - ' + s2[int(s2[j][6])-1][7] + ' - ' + s2[int(s2[int(s2[j][6])-1][6])-1][7] + '\n')
	file.write('\n')

	word_features = [w1gram, w2gram, w3gram]
	pos_features = [p2gram]#, p2gram, p3gram]
	dep_features = [d3gram]#, d2gram, d3gram]
	#word_features.extend(pos_features)
	#word_features.extend(dep_features)
	return word_features

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
	file = open('resultados_ms.txt', 'w+')
	pair_identification = []
	ms_features = []
	for pm in pair_matrixes:
		ms_features.append(ms_feature_calculator(pm[2],pm[3],[word,pos,dependency], file))
		pair_identification.append([pm[0], pm[1]])
	file.close()
	return pair_identification, np.array(ms_features)
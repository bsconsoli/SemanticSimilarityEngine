import parsers.MaltparserUniversalTreeBankPTBR.parse as mpp
import os
import numpy as np
import tempfile
import requests
from bs4 import BeautifulSoup

#PARSE VISL OUTPUT
def parse_visl(visl_parse):
	visl_info = visl_parse.split()
	visl_info[0] = visl_info[0].strip('<ß>')
	tokens = []
	token = []
	for info in visl_info:
		if info == '':
			continue
		if info[0] == '#':
			token.append(info)
			tokens.append(token)
			token = []
		else:
			token.append(info)
	parsed_tokens = ''
	for token in tokens:
		is_POS = False
		is_word = True
		node_id = '_'
		word = []
		lemma = '_'
		POS = '_'
		semantic_role = '_'
		father_node_id = '_'
		dependency_tag = '_'
		for t in token:
			if t[0] == '[' and t[-1] == ']':
				lemma = t[1:-1]
				is_POS = True
				is_word = False
				continue
			if t[0] == '<' and t[-1] == '>':
				continue
			if t[0] == '@':
				dependency_tag = t[1:]
				if t[1:] == 'PU':
					word = word[0]
					is_word = False
					POS = 'PU'
			if t[0] == '§':
				semantic_role = t[1:]
			if t[0] == '#':
				node_id = t[1:t.find('-')]
				father_node_id = t[t.find('>')+1:]
			if is_word:
				word.append(t)
			elif is_POS:
				POS = t
				is_POS = False
		parsed_tokens = parsed_tokens + '\t'.join([node_id,'_'.join(word),lemma,POS,semantic_role,'_',father_node_id,dependency_tag]) + '\n'
	return parsed_tokens


def get_ms_info(pair_matrix, parser):
	temp_array = []
	#IF MALTPARSER IS TO BE USED, THIS
	if parser == "maltparser":
		for i in range(pair_matrix.shape[0]):
			s1_file = tempfile.NamedTemporaryFile(prefix='s1.txt',
				dir=tempfile.gettempdir(), delete=False)
			s2_file = tempfile.NamedTemporaryFile(prefix='s2.txt',
				dir=tempfile.gettempdir(), delete=False)
			s1_file.write(bytes(pair_matrix[i, 1], "utf-8"))
			s2_file.write(bytes(pair_matrix[i, 2], "utf-8"))
			s1_file.close()
			s2_file.close()
			temp_array.append([pair_matrix[i,0],mpp.parse(s1_file.name),mpp.parse(s2_file.name),pair_matrix[i,3]])
			os.remove(s1_file.name)
			os.remove(s2_file.name)
	#IF VISL IS TO BE USED, THIS
	if parser == 'visl':
		url = 'https://visl.sdu.dk/visl/pt/parsing/automatic/dependency.php'
		for i in range(pair_matrix.shape[0]):

			payload = {'text' : pair_matrix[i, 1], 'parser' : 'roles', 'visual' : 'cg-dep', 'symbol' : 'unfiltered'}
			
			success = False
			while not success:
				r = requests.post(url, payload)
				html_soup = BeautifulSoup(r.content, 'html.parser')
				if html_soup.find('dl') != None:
					s1_parse = parse_visl(html_soup.find('dl').get_text())
					success = True

			payload = {'text' : pair_matrix[i, 2], 'parser' : 'roles', 'visual' : 'cg-dep', 'symbol' : 'unfiltered'}
			
			success = False
			while not success:
				r = requests.post(url, payload)
				html_soup = BeautifulSoup(r.content, 'html.parser')
				if html_soup.find('dl') != None:
					s2_parse = parse_visl(html_soup.find('dl').get_text())
					success = True

			temp_array.append([pair_matrix[i,0],s1_parse,s2_parse,pair_matrix[i,3]])
			print('Parsed: ' + pair_matrix[i][3])

	return np.array(temp_array)

import parsers.MaltparserUniversalTreeBankPTBR.parse as mpp
import os
import numpy as np
import tempfile
import requests
from bs4 import BeautifulSoup

def get_ms_info(pair_matrix, parser):
	temp_array = []
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
	if parser == 'visl':
		for i in range(pair_matrix.shape[0]):
			print(i)
			url = 'https://visl.sdu.dk/visl/pt/parsing/automatic/dependency.php'
			payload = {'text' : pair_matrix[i, 1], 'parser' : 'dep-eb', 'visual' : 'cg-dep', 'symbol' : 'unfiltered'}
			r = requests.post(url, payload)
			html_soup = BeautifulSoup(r.content, 'html.parser')
			print(html_soup.find('dl').get_text())
	return np.array(temp_array)

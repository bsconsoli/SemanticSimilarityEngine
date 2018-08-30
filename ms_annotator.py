import parsers.MaltparserUniversalTreeBankPTBR.parse as mpp
import os
import numpy as np
import tempfile

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
			
	return np.array(temp_array)

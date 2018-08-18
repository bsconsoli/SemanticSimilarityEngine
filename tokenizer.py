import parsers.MaltparserUniversalTreeBankPTBR.parse as mpp
import os

def get_ms_info(pair_matrix, parser):
	ms_info = mpp.parse()

ms_info = mpp.parse("/home/godfrey/Desktop/SemanticSimilarityEngine-develop/teste.txt")

print(ms_info.decode("utf-8"))

	
from collections import defaultdict
import operator

testfile = open("corpus_anotado_visl_test.txt")
trainfile = open("corpus_anotado_visl_train.txt")

sentencecount = 0
nosp = 0

spList = defaultdict(int)
for line in testfile.readlines():
	if line == '<\s1>\n' or line == '<\s2>\n': 
		if sentencecount == 0:
			nosp += 1
		sentencecount = 0
	if line[0] != '<' and line != '\n':
		info = line.split('\t')
		if info[4] != '_' and info[4] != 'REFL' and info[4] != 'MED' and info[4] != 'VOC' and info[4] != 'FOC' and info[4] != 'EV' and info[4] != 'PRED' and info[4] != '':
			sentencecount += 1
			spList[info[4]] += 1

for line in trainfile.readlines():
	if line[0] != '<' and line != '\n':
		info = line.split('\t')
		if info[4] != '_' and info[4] != 'REFL' and info[4] != 'MED' and info[4] != 'VOC' and info[4] != 'FOC' and info[4] != 'EV' and info[4] != 'PRED' and info[4] != '':
			spList[info[4]] += 1

allDict = spList.items()

print("No SP: ", nosp)

print(sorted(allDict, key=operator.itemgetter(1), reverse=True))
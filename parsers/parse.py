#!/usr/bin/python
# -*- coding: utf-8 -*-

#### Script to execute the mxpost and malparser to annotate a sentence sent from the input or by file
####
#### Some code borrowed from http://www.nltk.org/_modules/nltk/parse/malt.html

# Author: Pedro Balage (pedrobalage@gmail.com)
# Date: 25/05/2015
# Version: 1.0

#Modified by Bernardo Consoli (bernardo.consoli@acad.pucrs.br)
#17/08/2018
#For use with Semantic Similarity Engine

# imports
from subprocess import run, PIPE
import os

LEMATIZADOR_DIR = os.getcwd() + '/parsers/Lematizador/'

def parse(filename):
    print("Lematizing...")
    script = ["java", '-jar', 'lematizador.jar', filename]
    tok = run(script, cwd=(LEMATIZADOR_DIR), stdout=PIPE, stderr=PIPE)
    with open(filename + '.out') as f:
        lines = f.read().split(' ')
        sent = " ".join([s[:s.find('/')] for s in lines])
        lemma = [s[s.find('/')+1:] for s in lines]
    os.remove(filename + '.out')
    os.remove(filename + '.mxp')
    os.remove(filename + '.tagged')

    # MXPOST 
    p = run(['java', 
                '-mx30m', 
                '-cp', 
                'parsers/mxpost/mxpost.jar',
                'tagger.TestTagger',
                'parsers/pt-br-universal-tagger.project'], 
            input=bytes(sent, "utf-8"), stdout=PIPE)

    stdout = p.stdout
    sentences = stdout.decode("utf-8").split('\n')
    tokens = []
    for sentence in sentences:
        if not sentence == '\n':
            tokens.append([tuple(w.split('_')) for w in sentence.split()])
    sentences = tokens
    parsed_token_matrix = []
    try:
        lemma_counter = 0
        first = True
        for sentence in sentences:
            for (i, (word, tag)) in enumerate(sentence, start=1):
                if lemma[lemma_counter] == '//':
                    lemma_counter += 1
                input_str = '%s\t%s\t%s\t%s' %\
                    (i, word, lemma[lemma_counter], tag)
                lemma_counter += 1
                if i == 1 and not first:
                    parsed_token_matrix.append('')
                if first:
                    first = not first
                parsed_token_matrix.append(input_str)
        ms_info = '\n'.join(parsed_token_matrix)
    finally:
        return ms_info

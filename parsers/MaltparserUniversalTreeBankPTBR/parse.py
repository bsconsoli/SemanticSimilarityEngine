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

# Python 3 compatibility
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function

# imports
from subprocess import run, PIPE, Popen
import tempfile
import fileinput
import codecs
import os
import sys

LEMATIZADOR_DIR = os.getcwd() + '/parsers/MaltparserUniversalTreeBankPTBR/Lematizador/'

def parse(filename):
    sentences = []
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
                'parsers/MaltparserUniversalTreeBankPTBR/mxpost/mxpost.jar',
                'tagger.TestTagger',
                'parsers/MaltparserUniversalTreeBankPTBR/pt-br-universal-tagger.project'], 
            input=bytes(sent, "utf-8"), stdout=PIPE)

    stdout = p.stdout
    sentence = stdout.decode("utf-8")
    tokens = [tuple(w.split('_')) for w in sentence.split()]
    sentences.append(tokens)  
    tokens = []
    try:
        for sentence in sentences:
            for (i, (word, tag)) in enumerate(sentence, start=1):
                input_str = '%s\t%s\t%s\t%s' %\
                    (i, word, lemma[i-1], tag)
                tokens.append(input_str)
        ms_info = '\n'.join(tokens)
        print(ms_info)
    finally:
        return ms_info

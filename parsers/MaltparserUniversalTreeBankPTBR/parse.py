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

def parse(filename):
    sentences = []
    with open(filename) as f:
        line = f.read()
        # MXPOST 
        p = run(['java', 
                    '-mx30m', 
                    '-cp', 
                    'parsers/MaltparserUniversalTreeBankPTBR/mxpost/mxpost.jar',
                    'tagger.TestTagger',
                    'parsers/MaltparserUniversalTreeBankPTBR/pt-br-universal-tagger.project'], 
                input=bytes(line, "utf-8"), stdout=PIPE)

        stdout = p.stdout
        sentence = stdout.decode("utf-8")
        tokens = [tuple(w.split('_')) for w in sentence.split()]
        sentences.append(tokens)
        

    # MALT Parser
    input_file = tempfile.NamedTemporaryFile(prefix='malt_input.conll',
                                                    dir="parsers/MaltparserUniversalTreeBankPTBR/",
                                                    delete=False)
    output_file = tempfile.NamedTemporaryFile(prefix='malt_output.conll',
                                                    dir="parsers/MaltparserUniversalTreeBankPTBR/",
                                                    delete=False)

    try:
        for sentence in sentences:
            for (i, (word, tag)) in enumerate(sentence, start=1):
                input_str = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %\
                    (i, word, '_', tag, tag, '_', '0', 'a', '_', '_')
                input_file.write(input_str.encode("utf8"))
            input_file.write(b'\n\n')
        input_file.close()

        cmd = ['java' ,
                '-jar', 'maltparser-1.8.1/maltparser-1.8.1.jar',
                '-c'  , 'uni-dep-tb-ptbr', 
                '-i'  , input_file.name,
                '-o'  , output_file.name, 
                '-m'  , 'parse']

        p = Popen(cmd, cwd=(os.getcwd() + '/parsers/MaltparserUniversalTreeBankPTBR/'), stdout=PIPE, stderr=PIPE)
        ret = p.wait()


        ms_info = output_file.read()

    finally:
        input_file.close()
        os.remove(input_file.name)
        output_file.close()
        os.remove(output_file.name)
        return ms_info

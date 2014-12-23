#!/usr/bin/env python
#-*-coding:utf-8-*-

import sys
import os.path
import argparse

# path
script_path = os.path.dirname(__file__)
script_path = script_path if len(script_path) else '.'
sys.path.append(script_path + '/../src')

from poem_model import PoemModel
from poem_lda_model import PoemLdaModel
from poem_lsi_model import PoemLsiModel

# args
parser = argparse.ArgumentParser()
parser.add_argument('sentence')

if __name__ == '__main__':
    sentence = parser.parse_args().sentence
    # standard tf-idf model
    model = PoemModel()
    # model.construct()
    model.load()
    top_n = model.get_similar(sentence)
    for k, v in top_n: print k, v
    print '==='

    # lsi model
    lsi_model = PoemLsiModel()
    # lsi_model.construct()
    lsi_model.load()
    top_n = lsi_model.get_similar(sentence)
    for k, v in top_n: print k, v
    print '==='

    # lda model
    lda_model = PoemLdaModel()
    lda_model.construct()
    lda_model.load()
    top_n = lda_model.get_similar(sentence)
    for k, v in top_n: print k, v


#!/usr/bin/env python
#-*-coding:utf-8-*-

from gensim import corpora, models, similarities
import MeCab
import os.path
import re

cd = os.path.dirname(__file__)

class PoemModel(object):
    STOP_WORDS = ['・', '"', '\'', '-', '—', '×',
                  '「', '」', '…', '（', '）', '/', '／',
                  '０', '１', '２', '３', '４', '５', '６', '７', '８', '９']
    ACCEPTABLE_CATEGORIES = ['名詞', '動詞', '形容詞']

    _corpus = None
    _dictionary = None
    _index = None
    _model = None

    _data_path = '{0}/../data/mansion_poem_tokyo.tsv'.format(cd)
    _dictionary_path = '{0}/../model/poem.txt'.format(cd)
    _corpus_path = '{0}/../model/poem.mm'.format(cd)
    _index_path = '{0}/../model/poem.index'.format(cd)

    def __init__(self, load=True):
        self._data = self._load_row_data(self._data_path)

    def construct(self, no_below=1, no_above=0.4):
        sentences = ['{0} {1}'.format(row[-2], row[-1]) for row in self._data]
        words = [self._extract_words(s) for s in sentences]
        self._dictionary = self._create_dictionary(words, no_below, no_above)
        self._corpus = self._create_corpus(words)
        self._index = self._create_index()

    def load(self):
        self._dictionary = corpora.Dictionary.load_from_text(self._dictionary_path)
        self._corpus = corpora.MmCorpus(self._corpus_path)
        self._index = similarities.SparseMatrixSimilarity.load(self._index_path)

    def get_similar(self, sentence, n=10):
        words = self._extract_words(sentence)
        vec = self._dictionary.doc2bow(words)
        sims = self._index[vec]
        top_n = sorted(enumerate(sims), key=lambda item: -item[1])[:n]
        return [(self._data[k][1], v) for k, v in top_n]

    def _load_row_data(self, in_path):
        data = []
        for line in open(in_path).readlines():
            columns = [c.rstrip() for c in line.split('\t')]
            data.append(columns)
        return data

    def _extract_words(self, sentence):
        tagger = MeCab.Tagger()
        node = tagger.parseToNode(self._remove_stop_words(sentence))
        words = []
        while node:
            features = node.feature.split(",")
            if features[0] in self.ACCEPTABLE_CATEGORIES:
                word = node.surface.decode('utf-8') if features[6] == '*' else features[6]
                if re.match(r'\A[0-9]+\Z', word) is None: # remove word consist of only numbers
                    words.append(word.lower())
            node = node.next
        return words

    def _remove_stop_words(self, sentence):
        for word in self.STOP_WORDS:
            sentence = sentence.replace(word, ' ')
        return sentence

    def _create_dictionary(self, words, no_below=1, no_above=0.4):
        dictionary = corpora.Dictionary(words)
        dictionary.filter_extremes(no_below=no_below, no_above=no_above)
        dictionary.save_as_text(self._dictionary_path)
        return dictionary

    def _create_corpus(self, words):
        corpus = [self._dictionary.doc2bow(w) for w in words] # bag of words
        corpus = models.TfidfModel(corpus)[corpus] # apply tf-idf
        corpora.MmCorpus.serialize(self._corpus_path, corpus) # save serialize data
        return corpora.MmCorpus(self._corpus_path)

    def _create_index(self):
        index = similarities.MatrixSimilarity(self._corpus)
        index.save(self._index_path)
        return index
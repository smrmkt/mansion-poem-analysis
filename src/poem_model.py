#!/usr/bin/env python
#-*-coding:utf-8-*-

from gensim import corpora, models, similarities
import MeCab
import os.path
import re

cd = os.path.dirname(__file__)

class PoemModel(object):
    """
    CLASS CONSTANT

    STOP_WORDS: symbols and numbers have no meaning, so should be removed.
    ACCEPTABLE_CATEGORIES: these 3 categories seem to have outstanding characteristics
    """
    PRE_STOP_WORDS = ['・', '"', '\'', '-', '—', '×',
                      '「', '」', '…', '（', '）', '/', '／',
                      '０', '１', '２', '３', '４', '５', '６', '７', '８', '９']
    ACCEPTABLE_CATEGORIES = ['名詞', '動詞', '形容詞']

    _data_path = '{0}/../data/mansion_poem_tokyo.tsv'.format(cd)
    _stop_words_path = '{0}/../res/stop_words.txt'.format(cd)
    _dictionary_path = '{0}/../model/poem.txt'.format(cd)
    _corpus_path = '{0}/../model/poem.mm'.format(cd)
    _index_path = '{0}/../model/poem.index'.format(cd)

    def __init__(self):
        self._stop_words = [w.rstrip() for w in open(self._stop_words_path).readlines()]
        self._data = self._load_row_data()
        self._words = self._create_words()
        self._corpus = None
        self._dictionary = None
        self._index = None

    def construct(self, no_below=1, no_above=0.4):
        """
        this method is called when no model files exist.
        no_below: cut off minimum word count through all sentences
        no_above: cut off maximum percentage of sentences that contain specific word
        """
        self._dictionary = self._create_dictionary(self._words, no_below, no_above)
        self._corpus = self._create_corpus(self._words)
        self._index = self._create_index()

    def load(self):
        """
        load pre-constructed data
        """
        self._dictionary = corpora.Dictionary.load_from_text(self._dictionary_path)
        self._corpus = corpora.MmCorpus(self._corpus_path)
        self._index = similarities.SparseMatrixSimilarity.load(self._index_path)

    def get_similar(self, sentence, n=10):
        """
        obtains a list of mansion name and score
        sentence: target mansion poem to calculate similarity
        n: number of list elements
        return: list of mansion name and similarity score tuple
        """
        words = self._extract_words(sentence)
        vec = self._dictionary.doc2bow(words)
        sims = self._index[vec]
        top_n = sorted(enumerate(sims), key=lambda item: -item[1])[:n]
        return [(self._data[k][1], v) for k, v in top_n]

    @property
    def words(self):
        return self._words

    def _load_row_data(self):
        data = []
        for line in open(self._data_path).readlines():
            columns = [c.rstrip() for c in line.split('\t')]
            data.append(columns)
        return data

    def _create_words(self):
        sentences = ['{0} {1}'.format(row[-2], row[-1]) for row in self._data]
        return [self._extract_words(s) for s in sentences]

    def _extract_words(self, sentence):
        tagger = MeCab.Tagger()
        node = tagger.parseToNode(self._remove_pre_stop_words(sentence))
        words = []
        while node:
            features = node.feature.split(",")
            if features[0] in self.ACCEPTABLE_CATEGORIES:
                try:
                    word = node.surface.decode('utf-8') if features[6] == '*' else features[6]
                    if self._is_acceptable(word):
                        words.append(word.lower())
                except UnicodeDecodeError:
                    pass
            node = node.next
        return words

    def _is_acceptable(self, word):
        if re.match(r'\A[0-9]+\Z', word): # remove word consist of only numbers
            return False
        elif word in self._stop_words:
            return False
        else:
            return True

    def _remove_pre_stop_words(self, sentence):
        for word in self.PRE_STOP_WORDS:
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

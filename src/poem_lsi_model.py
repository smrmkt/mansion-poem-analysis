#!/usr/bin/env python
#-*-coding:utf-8-*-

from gensim import corpora, models, similarities
import os.path

from poem_model import PoemModel


class PoemLsiModel(PoemModel):
    _model = None
    _dictionary_path = os.path.dirname(__file__) + '/../model/lsi_poem.txt'
    _corpus_path = os.path.dirname(__file__) + '/../model/lsi_poem.mm'
    _index_path = os.path.dirname(__file__) + '/../model/lsi_poem.index'
    _model_path = os.path.dirname(__file__) + '/../model/lsi_poem.model'

    def __init__(self):
        super(PoemLsiModel, self).__init__()

    def construct(self, no_below=1, no_above=0.4, num_topics=20):
        sentences = ['{0} {1}'.format(row[-2], row[-1]) for row in self._data]
        words = [self._extract_words(s) for s in sentences]
        self._dictionary = self._create_dictionary(words, no_below, no_above)
        self._corpus = self._create_corpus(words)
        self._model = self._create_model(num_topics)
        self._index = self._create_index()

    def load(self):
        self._model = models.LsiModel.load(self._model_path)
        super(PoemLsiModel, self).load()

    def get_similar(self, sentence, n=10):
        words = self._extract_words(sentence)
        vec = self._model[self._dictionary.doc2bow(words)]
        sims = self._index[vec]
        top_n = sorted(enumerate(sims), key=lambda item: -item[1])[:n]
        return [(self._data[k][1], v) for k, v in top_n]

    def _create_model(self, num_topics):
        self._model = models.LsiModel(corpus=self._corpus,
                                      num_topics=num_topics,
                                      id2word=self._dictionary)
        self._model.save(self._model_path)
        return self._model

    def _create_index(self):
        index = similarities.MatrixSimilarity(self._model[self._corpus])
        index.save(self._index_path)
        return index

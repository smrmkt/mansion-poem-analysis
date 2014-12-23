#!/usr/bin/env python
#-*-coding:utf-8-*-

from gensim import models, similarities
import numpy as np
import os.path

from poem_model import PoemModel

cd = os.path.dirname(__file__)

class PoemLdaModel(PoemModel):
    _dictionary_path = '{0}/../model/lda_poem.txt'.format(cd)
    _corpus_path = '{0}/../model/lda_poem.mm'.format(cd)
    _index_path = '{0}/../model/lda_poem.index'.format(cd)
    _model_path = '{0}/../model/lda_poem.model'.format(cd)
    _feature_vector_path = '{0}/../model/lda_poem.csv'.format(cd)

    def __init__(self):
        self._feature_vector = None
        self._model = None
        super(PoemLdaModel, self).__init__()

    def construct(self, no_below=1, no_above=0.4, num_topics=20):
        sentences = ['{0} {1}'.format(row[-2], row[-1]) for row in self._data]
        words = [self._extract_words(s) for s in sentences]
        self._dictionary = self._create_dictionary(words, no_below, no_above)
        self._corpus = self._create_corpus(words)
        self._model = self._create_model(num_topics)
        self._index = self._create_index()
        self._feature_vector = self._create_feature_vector(words, num_topics)

    def load(self):
        self._model = models.LdaModel.load(self._model_path)
        self._feature_vector = np.loadtxt(self._feature_vector_path, delimiter=',')
        super(PoemLdaModel, self).load()

    def get_similar(self, sentence, n=10):
        words = self._extract_words(sentence)
        vec = self._model[self._dictionary.doc2bow(words)]
        sims = self._index[vec]
        top_n = sorted(enumerate(sims), key=lambda item: -item[1])[:n]
        return [(self._data[k][1], v) for k, v in top_n]

    @property
    def feature_vector(self):
        return self._feature_vector

    def _create_model(self, num_topics):
        self._model = models.LdaModel(corpus=self._corpus,
                                      num_topics=num_topics,
                                      id2word=self._dictionary)
        self._model.save(self._model_path)
        return self._model

    def _create_index(self):
        index = similarities.MatrixSimilarity(self._model[self._corpus])
        index.save(self._index_path)
        return index

    def _create_feature_vector(self, words, num_topics):
        feature_vector = []
        for w in words:
            v = [0.0]*num_topics
            for kv in self._model[self._dictionary.doc2bow(w)]:
                v[kv[0]] = kv[1]
            feature_vector.append(v)
        feature_vector = np.array(feature_vector)
        np.savetxt(self._feature_vector_path, feature_vector, delimiter=',')
        return feature_vector
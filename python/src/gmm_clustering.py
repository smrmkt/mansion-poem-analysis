#!/usr/bin/env python
#-*-coding:utf-8-*-

from sklearn.mixture import GMM
import itertools
import numpy as np

class GmmClustering():
    COVARIANCE_TYPES = ['spherical', 'tied', 'diag', 'full']

    def __init__(self, feature_vector):
        self._feature_vector = feature_vector
        self._model = None

    def fit_gmm(self, num_clusters, **kwargs):
        args = list(itertools.product(self.COVARIANCE_TYPES, range(1, num_clusters+1)))
        models = np.zeros(len(args), dtype=object)
        for i, (covariance_type, n) in enumerate(args):
            models[i] = GMM(n, covariance_type=covariance_type, **kwargs)
            models[i].fit(self._feature_vector)
        # return minimum aic model
        aic = np.array([m.aic(self._feature_vector) for m in models])
        self._model = models[np.argmin(aic)]

    def get_cluster_label(self):
        return self._model.predict(self._feature_vector)

    def predict(self, new_feature):
        return self._model.predict(new_feature)
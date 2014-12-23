#!/usr/bin/env python
#-*-coding:utf-8-*-

import argparse
import os
import os.path
import sys
import shutil

# encode
reload(sys)
sys.setdefaultencoding("utf-8")

# path
script_path = os.path.dirname(__file__)
script_path = script_path if len(script_path) else '.'
sys.path.append(script_path + '/../src')

out_path = '{0}/../out/words'.format(script_path)

from gmm_clustering import GmmClustering
from poem_lda_model import PoemLdaModel

# args
parser = argparse.ArgumentParser()
parser.add_argument('num_cluster', type=int)
parser.add_argument('no_below', type=int, default=1)
parser.add_argument('no_above', type=float, default=0.4)

if __name__ == '__main__':
    num_cluster = parser.parse_args().num_cluster
    no_below = parser.parse_args().no_below
    no_above = parser.parse_args().no_above

    # get LDA feature data
    lda_model = PoemLdaModel()
    lda_model.construct(no_below=no_below, no_above=no_above)
    # lda_model.load()

    # conduct gmm clustering and get label
    gmm = GmmClustering(lda_model.feature_vector)
    gmm.fit_gmm(num_cluster)
    labels = gmm.get_cluster_label()
    shutil.rmtree(out_path)
    os.mkdir(out_path)
    with open('{0}/label.txt'.format(out_path), 'w') as f:
        f.write('\n'.join(['{0}\t{1}'.format(k, v) for k, v in enumerate(labels)]))

    # write out words used in each cluster
    words_by_clusters = [[] for i in range(num_cluster)]
    for i, words in enumerate(lda_model.words):
        words_by_clusters[labels[i]].extend(words)
    sentences_by_clusters = ['\n'.join(words) for words in words_by_clusters]
    for i in range(num_cluster):
        with open('{0}/cluster{1}.txt'.format(out_path, i), 'w') as f:
            f.write(sentences_by_clusters[i])

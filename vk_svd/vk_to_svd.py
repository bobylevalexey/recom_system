import os
from itertools import product

from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction import DictVectorizer
import numpy as np

from svd.base import DictModel
from rs_config import DATA_DIR
from model import connect
from vk_svd.features import get_features


def _replace_nones(matr, val):
    print matr.shape
    for i, j in product(xrange(matr.shape[0]), xrange(matr.shape[1])):
        if np.isnan(matr[i, j]):
            matr[i, j] = val

if __name__ == "__main__":
    connect()

    model = DictModel(0)
    model.load(os.path.join(DATA_DIR, 'model.json'))

    model_user_ids = model.U_matr.keys()
    ids, features = get_features(model_user_ids)
    print len(ids), len(features)


    d = DictVectorizer(sparse=False)
    data_set = d.fit_transform(features)
    print data_set.shape
    print len([model.U_matr[id_][0] for id_ in ids])
    # exit()
    _replace_nones(data_set, -10)
    l = LinearRegression(normalize=False)

    l.fit(data_set, [model.U_matr[id_][0] for id_ in ids])
    #
    # print d.get_feature_names()

    # # l.fit([(1, 4)], [3])
    print l.coef_
    # print l.predict((1, 7))

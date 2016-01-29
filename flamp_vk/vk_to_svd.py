import os
from itertools import product

import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from svd.base import DictModel

from flamp_vk.get_vk_features import get_vk_users_features
from model import connect
from rs_config import DATA_DIR


class VkToSvd(object):
    def __init__(self, factors_num):
        self.factors_num = factors_num
        self.model = LinearRegression()
        self.vectorizer = DictVectorizer(sparse=False)

    def train(self, features_dict, U_matr):
        all_ids = set(features_dict.keys()) & set(U_matr.keys())
        features_matr = []
        vectors_matr = []
        ids_dict = {}
        for idx, id_ in enumerate(all_ids):
            features_matr.append(features_dict[id_])
            vectors_matr.append(U_matr[id_])
            ids_dict[id_] = idx
        X = self.vectorizer.fit_transform(
            features_matr, vectors_matr)
        _replace_nones(X, -100)
        self.model.fit(X, vectors_matr)
        return self.model.score(X, vectors_matr)

    def get_vect_dict(self, features_dict):
        return {
            id_: self.get_vect(features)
            for id_, features in features_dict.iteritems()
        }

    def get_vect(self, features):
        vectorized_features = _replace_nones(
            self.vectorizer.transform([features]), -100)[0]
        return vectorized_features.dot(self.model.coef_.transpose())


def _replace_nones(matr, val):
    for i, j in product(xrange(matr.shape[0]), xrange(matr.shape[1])):
        if np.isnan(matr[i, j]):
            matr[i, j] = val
    return matr

if __name__ == "__main__":
    from flamp_vk.get_marks import get_marks_list_from_db
    connect()

    model = DictModel(0)
    model.load(os.path.join(DATA_DIR, 'model.json'))

    features = get_vk_users_features()

    m = VkToSvd(model.factors_num)
    m.train(features, model.U_matr)
    m.get_vect(features.values()[0])

    new_model = DictModel(
        model.factors_num, m.get_vect_dict(features), model.V_matr)
    print new_model.calc_rmse(get_marks_list_from_db())

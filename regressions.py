# coding=utf-8
import math
from abc import abstractmethod, ABCMeta

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression, LinearRegression

from utils import replace_nones


class Model(object):
    __metaclass__ = ABCMeta

    def __init__(self, options=None):
        options = options or {}
        self.model = self.create_model(**options)

    @staticmethod
    def get_feature_dict(feature, matr_dict, features):
        return {id_: features[id_][feature] for id_ in features
                if features[id_][feature] is not None and
                id_ in matr_dict}

    @abstractmethod
    def get_err(self, x_test, y_test):
        pass

    @abstractmethod
    def create_model(self, **options):
        pass

    def to_xy(self, matr_dict, features_dict, ids=None):
        ids = ids or features_dict.keys()
        return [matr_dict[id_] for id_ in ids],\
               [features_dict[id_] for id_ in ids]

    def train(self, matr_dict, features_dict):
        """
        svd_model and features_dict must have same keys
        """
        X, Y = self.to_xy(matr_dict, features_dict)

        self.model.fit(X, Y)

        return {
            'err': self.get_err(X, Y),
            'coef': self.model.coef_.tolist()
        }


class LogisticModel(Model):
    def create_model(self, **options):
        return LogisticRegression(**options)

    def get_err(self, x_test, y_test):
        return (sum(pr != y for pr, y in zip(
                    self.model.predict(x_test), y_test)) /
                float(len(y_test)))


class LinearModel(Model):
    def create_model(self, **options):
        return LinearRegression(**options)

    def get_err(self, x_test, y_test):
        return math.sqrt((sum((pr - y)**2 for pr, y in zip(
                              self.model.predict(x_test), y_test)) /
                          float(len(y_test))))


class FeaturesToSvd(object):
    def __init__(self, factors_num, replacing_val=-100):
        self.factors_num = factors_num
        self.model = LinearRegression()
        self.vectorizer = DictVectorizer(sparse=False)
        self.replacing_val = replacing_val

    def train(self, features_dict, matr_dict):
        all_ids = set(features_dict.keys()) & set(matr_dict.keys())
        features_matr = []
        vectors_matr = []
        ids_dict = {}
        for idx, id_ in enumerate(all_ids):
            features_matr.append(features_dict[id_])
            vectors_matr.append(matr_dict[id_])
            ids_dict[id_] = idx
        X = self.vectorizer.fit_transform(
            features_matr)
        replace_nones(X, self.replacing_val)
        self.model.fit(X, vectors_matr)
        return self.model.score(X, vectors_matr)

    def get_vect_dict(self, features_dict):
        return {
            id_: self.get_vect(features)
            for id_, features in features_dict.iteritems()
        }

    def get_vect(self, features):
        vectorized_features = replace_nones(
            self.vectorizer.transform([features]), self.replacing_val)[0]
        return vectorized_features.dot(self.model.coef_.transpose())

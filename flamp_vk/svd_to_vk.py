# coding=utf-8
import json
import math
import os
from abc import abstractmethod, ABCMeta
from itertools import product

from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression
from svd.base import DictModel

from flamp_vk.get_marks import get_marks_list_from_db
from flamp_vk.get_vk_features import get_vk_users_features
from model import connect, get_dict
from rs_config import DATA_DIR
from tables import FlampExpertsTable
from utils import frange


class Model(object):
    __metaclass__ = ABCMeta

    def __init__(self, options=None):
        options = options or {}
        self.model = self.create_model(**options)

    @staticmethod
    def get_feature_dict(feature, svd_model, features, marks_counts,
                         min_marks=0):
        return {id_: features[id_][feature] for id_ in features
                if features[id_][feature] is not None and
                id_ in svd_model.U_matr and marks_counts[id_] >= min_marks}

    @abstractmethod
    def get_err(self, x_test, y_test):
        pass

    @abstractmethod
    def create_model(self, **options):
        pass

    def train(self, svd_model, features_dict, train_size=0.7):
        """
        svd_model and features_dict must have same keys
        """
        x = [svd_model.U_matr[id_] for id_ in features_dict]
        y = [features_dict[id_] for id_ in features_dict]

        x_train, x_test, y_train, y_test = train_test_split(
                x, y, train_size=train_size)

        self.model.fit(x_train, y_train)

        return {
            'err': self.get_err(x_test, y_test),
            'train_size': len(y_train),
            'test_size': len(y_test),
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
        for pr, y in zip(self.model.predict(x_test), y_test):
            print pr, y
        return math.sqrt((sum((pr - y)**2 for pr, y in zip(
                              self.model.predict(x_test), y_test)) /
                          float(len(y_test))))


def test_feature(feature, svd_model, features, marks_counts, attempts=10,
                 C_range=None, min_marks_range=None):
    attempts = attempts
    C_range = C_range or frange(0.1, 1., 0.1)
    min_marks_range = min_marks_range or xrange(1, 15)

    results = []
    for min_marks, C in product(min_marks_range, C_range):
        features_dict = Model.get_feature_dict(
            feature, svd_model, features, marks_counts, min_marks)
        for attempt_idx in xrange(attempts):
            print attempt_idx + 1, feature, min_marks, C
            report = LogisticModel({'C': C}).train(svd_model, features_dict)

            results.append({
                'C': C,
                'feature': feature,
                'min_marks': min_marks,
                'attempt_idx': attempt_idx + 1,
                'train_size': report['train_size'],
                'test_size': report['test_size'],
                'err': report['err'],
                'coef': report['coef']
            })
    return results


def test_vk_classified_features(svd_model, features, marks_counts):
    results = []
    looking_features = ['political', 'life_main', 'people_main', 'alcohol',
                        'smoking', 'relation', 'occupation_type']
    for feature in looking_features:
        results.extend(test_feature(feature, svd_model, features, marks_counts))
    with open(os.path.join(DATA_DIR, 'logistic_results.json'), 'w') as f:
        json.dump(results, f)


def test_sex(svd_model, marks_count):
    # костыль
    sex_dict = {d['id_']: {'sex': d['sex']}
                for d in get_dict(FlampExpertsTable, {'id_', 'sex'})}
    results = test_feature('sex', svd_model, sex_dict, user_marks,
                           min_marks_range=xrange(1, 30))
    with open(os.path.join(DATA_DIR, 'sex_logistic_regression.json'), 'w') as f:
        json.dump(results, f)

if __name__ == "__main__":
    connect()

    model = DictModel(0)
    model.load(os.path.join(DATA_DIR, 'model.json'))
    features = get_vk_users_features()
    marks = get_marks_list_from_db()
    user_marks = {}

    for u_id, i_id, mark in marks:
        user_marks[u_id] = user_marks.get(u_id, 0) + 1

    married_feature = {}
    for id_ in features:
        rel = features[id_]['relation']
        married = None
        if rel is not None:
            if rel == 'married':
                married = 1
            elif rel != 'undef':
                married = 0
        if married is not None:
            married_feature[id_] = {'married': married}

    print LogisticModel().train(model, Model.get_feature_dict(
        'married', model, married_feature, user_marks, min_marks=1
    ))

    # print LinearModel().train(model, Model.get_feature_dict(
    #     'age', model, features, user_marks, min_marks=5
    # ))
    # test_sex(model, user_marks)

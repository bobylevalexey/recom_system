# coding=utf-8
import os
import json
from abc import abstractmethod, ABCMeta
from itertools import product

from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression

from model import connect, get_dict
from rs_config import DATA_DIR
from svd.base import DictModel
from svd.utils import frange
from svd.create_svd_input import get_marks_list_from_db
from vk_svd.features import get_vk_users_features
from tables import FlampExpertsTable


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
    results = test_feature('sex', model, sex_dict, user_marks,
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

    test_sex(model, user_marks)

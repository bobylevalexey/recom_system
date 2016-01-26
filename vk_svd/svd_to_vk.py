import os
import json

from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression

from model import connect, get_dict
from rs_config import DATA_DIR
from svd.base import DictModel
from svd.create_svd_input import get_marks_list_from_db
from vk_svd.features import get_vk_users_features
from tables import FlampExpertsTable


def logistic_model(model, features, feature, marks_counts, min_marks=0,
                   options=None):
    ids = [
        id_ for id_ in features
        if features[id_][feature] is not None and id_ in model.U_matr and
        marks_counts[id_] >= min_marks]

    x = [model.U_matr[id_] for id_ in ids]
    y = [features[id_][feature] for id_ in ids]

    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.7)

    options = options or {}
    l = LogisticRegression(**options)
    l.fit(x_train, y_train)

    err = (sum(pr == y for pr, y in zip(l.predict(x_test), y_test)) /
           float(len(y_test)))
    return {
        'err': err,
        'model': l,
        'train_size': len(y_train),
        'test_size': len(y_test),
    }

if __name__ == "__main__":
    connect()

    model = DictModel(0)
    model.load(os.path.join(DATA_DIR, 'model.json'))
    features = get_vk_users_features()
    marks = get_marks_list_from_db()
    user_marks = {}
    for u_id, i_id, mark in marks:
        user_marks[u_id] = user_marks.get(u_id, 0) + 1

    print logistic_model(model, features, 'life_main', user_marks, 1,
                         {'C': 1})

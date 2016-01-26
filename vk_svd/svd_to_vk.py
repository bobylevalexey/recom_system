import os

from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression

from model import connect, get_dict
from rs_config import DATA_DIR
from svd.base import DictModel
from svd.create_svd_input import get_marks_list_from_db
from vk_svd.features import get_vk_users_features
from tables import FlampExpertsTable

if __name__ == "__main__":
    connect()

    model = DictModel(0)
    model.load(os.path.join(DATA_DIR, 'model.json'))

    marks = get_marks_list_from_db()
    user_marks = {}
    for u_id, i_id, mark in marks:
        user_marks[u_id] = user_marks.get(u_id, 0) + 1

    ids_and_sex = {dict_['id_']: dict_['sex']
                   for dict_ in get_dict(FlampExpertsTable, ['id_', 'sex'])}

    features = get_vk_users_features()
    ids = [
        id_ for id_ in ids_and_sex
        if ids_and_sex[id_] is not None and user_marks.get(id_, -1) > 12
        and id_ in model.U_matr]
    print len(ids)
    sex_codes = {
        'female': 1,
        'male': 0
    }
    x = [model.U_matr[id_] for id_ in ids]
    y = [sex_codes[ids_and_sex[id_]] for id_ in ids]

    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.7)

    l = LogisticRegression()
    l.fit(x_train, y_train)

    print (sum(abs(pr - y) for pr, y in zip(l.predict(x_test), y_test)) /
           float(len(y_test)))

import os

from sklearn.linear_model import LogisticRegression

from model import connect
from rs_config import DATA_DIR
from svd.base import DictModel
from vk_svd.features import get_vk_users_features

if __name__ == "__main__":
    connect()

    model = DictModel(0)
    model.load(os.path.join(DATA_DIR, 'model.json'))

    features = get_vk_users_features()
    ids_with_sex = [
        id_ for id_ in features
        if features[id_]['sex'] in ['male', 'female'] and id_ in model.U_matr]
    x = [model.U_matr[id_] for id_ in ids_with_sex]
    sex_codes = {
        'female': 1,
        'male': 0
    }
    y = [sex_codes[features[id_]['sex']] for id_ in ids_with_sex]

    l = LogisticRegression()
    l.fit(x, y)
    print l.predict([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

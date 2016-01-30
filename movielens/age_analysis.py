import os

from sklearn.cross_validation import train_test_split

from model import connect
from regressions import LinearModel
from svd_model import DictModel
from rs_config import ML_DATA_DIR
from movielens.get_features import get_users_features

if __name__ == "__main__":
    connect()
    ml_model = DictModel()
    ml_model.load(os.path.join(ML_DATA_DIR, 'model.json'))
    ages = {id_: dict_['age']
            for id_, dict_ in get_users_features().iteritems()}

    l = LinearModel()
    train_ids, test_ids = train_test_split(ages.keys(), train_size=0.7)
    print l.train(ml_model.U_matr, ages, train_ids)
    print l.get_err_from_dicts(ml_model.U_matr, ages, test_ids)

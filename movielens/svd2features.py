import os

from model import connect
from regressions import LinearModel, LogisticModel
from svd_model import DictModel
from rs_config import ML_DATA_DIR
from movielens.get_features import get_users_features


OCCUPATIONS = ['administrator', 'artist', 'doctor', 'educator', 'engineer',
               'entertainment', 'executive', 'healthcare', 'homemaker',
               'lawyer', 'librarian', 'marketing', 'none', 'other',
               'programmer', 'retired', 'salesman', 'scientist', 'student',
               'technician', 'writer']


def check_occupation(svd, features, occupations=None):
    occupations = occupations or OCCUPATIONS
    l = LogisticModel()
    occup_dict = {}
    for id_, occup in l.get_feature_dict('occupation', ml_model.U_matr,
                                         u_features).iteritems():
        occup_dict[id_] = occup if occup in occupations else 'undef'
    print l.train(ml_model.U_matr, occup_dict)
    def get_err_by_occup(occupation):
        return l.get_err(*l.to_xy(ml_model.U_matr, occup_dict,
                                  [id_ for id_, occup in occup_dict.iteritems()
                                   if occup == occupation]))
    for occup in occupations:
        print occup, get_err_by_occup(occup)


def check_singe_occup(svd, features, occupation):
    l = LogisticModel()
    is_student_feature = {id_: bool(f['occupation'] == occupation)
                          for id_, f in features.iteritems()}
    print l.train(svd.U_matr, is_student_feature)  # err: 0.20785

if __name__ == "__main__":
    connect()
    ml_model = DictModel()
    ml_model.load(os.path.join(ML_DATA_DIR, 'model.json'))
    u_features = get_users_features()

    check_occupation(ml_model, u_features)
    check_singe_occup(ml_model, u_features, 'student')
    check_singe_occup(ml_model, u_features, 'educator')

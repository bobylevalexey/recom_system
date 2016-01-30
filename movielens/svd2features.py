import os

from sklearn.cross_validation import train_test_split

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


def check_occupation(svd, features, occupations=None, train_size=0.7):
    occupations = occupations or OCCUPATIONS
    l = LogisticModel()
    occup_dict = {}
    for id_, occup in l.get_feature_dict('occupation', ml_model.U_matr,
                                         u_features).iteritems():
        occup_dict[id_] = occup if occup in occupations else 'undef'
    ids_train, ids_test = train_test_split(occup_dict.keys(),
                                           train_size=train_size)
    print l.train(ml_model.U_matr, occup_dict, ids_train)
    print l.get_err(*l.to_xy(ml_model.U_matr, occup_dict, ids_test))

    def get_err_by_occup(occupation, ids):
        return l.get_err(*l.to_xy(ml_model.U_matr, occup_dict,
                                  set(id_
                                      for id_, occup in occup_dict.iteritems()
                                      if occup == occupation) & set(ids)))
    for occup in occupations:
        print occup, get_err_by_occup(occup, ids_train),\
            get_err_by_occup(occup, ids_test)


def check_singe_occup(svd, features, occupation, train_size=0.7):
    l = LogisticModel()
    is_student_feature = {id_: bool(f['occupation'] == occupation)
                          for id_, f in features.iteritems()}
    ids_train, ids_test = train_test_split(features.keys(),
                                           train_size=train_size)
    print l.train(svd.U_matr, is_student_feature, ids_train)
    print l.get_err(*l.to_xy(svd.U_matr, is_student_feature, ids_test))


def print_sep():
    print
    print '-----------------'
    print

if __name__ == "__main__":
    connect()
    ml_model = DictModel()
    ml_model.load(os.path.join(ML_DATA_DIR, 'model.json'))
    u_features = get_users_features()

    check_occupation(ml_model, u_features)
    print_sep()
    for occup in OCCUPATIONS:
        print occup
        check_singe_occup(ml_model, u_features, occup)
        print_sep()

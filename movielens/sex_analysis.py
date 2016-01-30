import os

from sklearn.cross_validation import train_test_split

from model import connect
from regressions import LogisticModel, LinearModel
from svd_model import DictModel
from movielens.config import ML_DATA_DIR
from movielens.get_features import get_users_features
from utils import frange
from params_finder import ParamsFinder
from view_reports import get_max_min_avg, view_results


class SexPramsFinder(ParamsFinder):
    def __init__(self, sex_dict, attempts=10):
        super(SexPramsFinder, self).__init__(attempts)
        self.sex_dict = sex_dict

    def get_trainer(self, cls, options):
        return cls(options)

    def train_model(self, train_data, test_data, model, trainer):
        tr_err = trainer.train(model.U_matr, self.sex_dict, train_data)
        test_err = trainer.get_err_from_dicts(
            model.U_matr, self.sex_dict, test_data)
        return {
            'train_err': tr_err,
            'test_err': test_err
        }


if __name__ == "__main__":
    connect()
    ml_model = DictModel()
    ml_model.load(os.path.join(ML_DATA_DIR, 'model.json'))
    sex_dict = {id_: dict_['sex']
                for id_, dict_ in get_users_features().iteritems()}

    p = SexPramsFinder(sex_dict)
    p.find(sex_dict.keys(), LogisticModel, [(ml_model, 'simp')],
           {'C': frange(0.01, 0.1, 0.01)}, ())
    view_results(p.reports,
                 '{test_err_avg:<20} {min_test_err:<20} '
                 '{max_test_err:<20} {C:<20} {orig_dict}', aggr_by='test_err',
                 sort_by='test_err_avg')

import math
import os

from sklearn.cross_validation import train_test_split
from svd_model import DictModel

from flamp_vk.get_svd_model import RSVD
from model import connect
from movielens.get_marks import get_ml_marks
from params_finder import ParamsFinder
from movielens.config import ML_DATA_DIR
from utils import frange


class RSVDParamsFinder(ParamsFinder):
    def train_model(self, train_data, test_data, model, trainer):
        new_model = trainer.train(model, train_data)
        train_err = new_model.calc_rmse(train_data)
        test_err = new_model.calc_rmse(test_data)
        return {'train_err': train_err,
                'test_err': test_err}

if __name__ == "__main__":
    connect()

    marks = get_ml_marks()

    train_marks, test_marks = train_test_split(marks, train_size=0.7)

    lrate = 0.009
    acc = 1
    reg = 0.1
    factors_num = 10
    max_epochs = 5000
    init_val = math.sqrt(3. / factors_num)
    deep_copy = True
    glob_epochs = 1

    ranges = {
        'reg': frange(0.08, 0.1, 0.01),
        'lrate': frange(0.005, 0.01, 0.001)
    }
    static_params = {
        'acc': 1,
        'max_epochs': 5000,
        'deep_copy': True,
        'glob_epochs': 1
    }

    model = DictModel(factors_num).with_val(init_val)\
        .init_from_marks_list(marks)

    # RSVDParamsFinder(5).find(
    #     marks, RSVD, [(model, 'simp')], ranges, static_params,
    #     dump_to=os.path.join(DATA_DIR, 'ml_rsvd_params_report.json'))

    svd = RSVD(reg=reg, acc=acc, lrate=lrate, max_epochs=max_epochs,
               deep_copy=deep_copy, glob_epochs=glob_epochs)
    model = svd.train(model, train_marks)
    model.dump(os.path.join(ML_DATA_DIR, 'model.json'))
    print model.calc_rmse(train_marks)
    print model.calc_rmse(test_marks)

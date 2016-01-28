import math

from sklearn.cross_validation import train_test_split

from svd.rsvd import RSVD
from svd.base import DictModel
from rs_config import DATA_DIR
from model import connect
from movielens.get_marks import get_ml_marks


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

    model = DictModel(factors_num).with_val(init_val)\
        .init_from_marks_list(marks)

    svd = RSVD(reg=reg, acc=acc, lrate=lrate, max_epochs=max_epochs,
               deep_copy=deep_copy, glob_epochs=glob_epochs)
    model = svd.train(model, train_marks)
    # model.dump(os.path.join(DATA_DIR, 'model.json'))
    print model.calc_rmse(train_marks)
    print model.calc_rmse(test_marks)


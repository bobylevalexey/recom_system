# coding=utf-8
import math

from svd_model import DictModel
from rsvd import RSVD


if __name__ == "__main__":
    import os

    from get_marks import get_marks_list_from_db
    from model import connect
    from rs_config import DATA_DIR

    connect()
    marks = get_marks_list_from_db()
    marks_avg = sum(m for u_id, i_id, m in marks) / float(len(marks))

    lrate = 0.009
    acc = 1
    reg = 0.1
    factors_num = 10
    max_epochs = 5000
    init_val = math.sqrt(3. / factors_num)
    deep_copy = True
    glob_epochs = 1

    model = DictModel(factors_num).with_val(
            init_val).init_from_marks_list(marks)

    svd = RSVD(reg=reg, acc=acc, lrate=lrate, max_epochs=max_epochs,
               deep_copy=deep_copy, glob_epochs=glob_epochs)
    model = svd.train(model, marks)
    model.dump(os.path.join(DATA_DIR, 'model.json'))
    print model.calc_rmse(marks)

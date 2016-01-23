import math
from sklearn.cross_validation import train_test_split

from svd.base import DictModel
from svd.rsvd import RSVD

if __name__ == "__main__":
    import time

    from create_svd_input import get_marks_list_from_db
    from model import connect
    from svd.utils import frange

    connect()

    lrate = 0.009
    acc = 10
    reg = 0.1
    factors_num = 10
    max_epochs = 5000
    train_size = 0.7
    init_val = math.sqrt(3. / factors_num)
    deep_copy = True
    glob_epochs = 1

    marks = get_marks_list_from_db()
    train, test = train_test_split(marks, train_size=train_size)
    model = DictModel(factors_num).with_val(
        math.sqrt(3. / factors_num)).init_from_marks_list(train)

    results = []
    for glob_epochs in xrange(1, 10, 1):
        svd = RSVD(reg=reg, acc=acc, lrate=lrate, max_epochs=max_epochs,
                   deep_copy=deep_copy, glob_epochs=glob_epochs)
        st = time.time()
        tr_model = svd.train(model, train)
        report = {
            'lrate': lrate,
            'acc': acc,
            'reg': reg,
            'fn': factors_num,
            'dp': int(deep_copy),
            'train': "%.5f" % tr_model.calc_rmse(train),
            'test': "%.5f" % tr_model.calc_rmse(test),
        }
        results.append(report)

        print 'res', report
    for res in results:
        print res

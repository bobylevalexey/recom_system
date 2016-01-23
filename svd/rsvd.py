# coding=utf-8
import logging
from copy import deepcopy

import math
from sklearn.cross_validation import train_test_split

from base import DictModel


class RSVD(object):
    def __init__(self, lrate=0.035, reg=0.01, max_epochs=30, acc=0.001,
                 glob_epochs=1, deep_copy=False):
        self.lrate = lrate
        self.reg = reg
        self.acc = acc
        self.max_epochs = max_epochs
        self.glob_epochs = glob_epochs
        self.deep_copy = deep_copy

        # tmp variables
        self._train_marks = None
        self._train_model = None

    def train_k_factor(self, k):
        sse = 0.0
        if self.deep_copy:
            new_model = deepcopy(self._train_model)
        else:
            new_model = self._train_model
        for user_id, item_id, mark in self._train_marks:
            err = mark - new_model.predict(user_id, item_id)
            sse += err**2

            old_pik = new_model.U_matr[user_id][k]
            old_qjk = new_model.V_matr[item_id][k]

            new_model.U_matr[user_id][k] += \
                self.lrate * (err * old_qjk - self.reg * old_pik)
            new_model.V_matr[item_id][k] += \
                self.lrate * (err * old_pik - self.reg * old_qjk)
        return new_model, sse + self.reg * (self.matr_sqr_sum(new_model.U_matr) +
                                            self.matr_sqr_sum(new_model.V_matr))

    def matr_sqr_sum(self, matr):
        return sum(sum(fact**2 for fact in vect)
                   for vect in model.U_matr.values())

    def train(self, model, marks):
        self._train_model = deepcopy(model)
        self._train_marks = marks

        old_loss = float('inf')
        for glob_epoch in xrange(self.glob_epochs):
            print "glob epoch=", glob_epoch
            for k in range(self._train_model.factors_num):
                print "k=", k
                for epoch in range(self.max_epochs):
                    new_model, new_loss = self.train_k_factor(k)

                    print "epoch=", epoch, "; dif=", old_loss - new_loss, \
                        "; loss=", new_loss
                    # check if train error is still changing
                    if old_loss - new_loss < self.acc:
                        print 'stoping'
                        break
                    self._train_model = new_model
                    old_loss = new_loss

        return self._train_model

if __name__ == "__main__":
    import time

    from create_svd_input import get_marks_list_from_db
    from model import connect
    from svd.utils import frange

    connect()
    logging.basicConfig(level=logging.INFO)

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

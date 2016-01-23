# coding=utf-8
import logging
import random
from abc import ABCMeta, abstractmethod
import math
from copy import deepcopy
import functools

from svd.utils import dot_product


class DictModel(object):
    def __init__(self, factors_num, U=None, V=None):
        self.factors_num = factors_num
        self.U_matr = U or {}
        self.V_matr = V or {}

        self.init_func = lambda: 1

    def with_reals(self, *bounds):
        self.init_func = functools.partial(random.uniform, *bounds)
        return self

    def with_avg(self):
        init_val = 5. / self.factors_num
        self.init_func = lambda: init_val
        return self

    def with_sqrt_avg(self):
        init_val = math.sqrt(5. / self.factors_num)
        self.init_func = lambda: init_val
        return self

    def with_val(self, val):
        self.init_func = lambda: val
        return self

    def init_from_marks_list(self, marks):
        self.U_matr = {user_id: [self.init_func()
                                 for _ in xrange(self.factors_num)]
                       for user_id in set(user_id
                                          for user_id, item_id, mark in marks)}
        self.V_matr = {item_id: [self.init_func()
                                 for _ in xrange(self.factors_num)]
                       for item_id in set(item_id
                                          for user_id, item_id, mark in marks)}
        return self

    def predict(self, user_id, item_id):
        """
        raises KeyError if user_id or item_id doesn't present in model
        :param user_id:
        :param item_id:
        """
        prediction = dot_product(self.U_matr[user_id], self.V_matr[item_id])
        if prediction < 1:
            return 1
        if prediction > 5:
            return 5
        return prediction

    def calc_rmse(self, marks):
        sqr_err = 0
        marks_found = 0
        for user_id, item_id, mark in marks:
            try:
                predict = self.predict(user_id, item_id)
                sqr_err += (mark - predict) ** 2
                marks_found += 1
            except KeyError:
                pass
        return math.sqrt(float(sqr_err) / marks_found)


class BaseRSVD(object):
    __metaclass__ = ABCMeta

    LOGGER = logging.getLogger('base')

    def __init__(self, lrate, reg, max_epochs, acc):
        self.lrate = lrate
        self.reg = reg
        self.max_epochs = max_epochs
        self.acc = acc

        # tmp variables
        self.train_marks = None

    @abstractmethod
    def train_epoch(self, model):
        return model

    def d_uk(self, user_id, k, model, marks=None):
        marks = marks or self.train_marks
        err = 0
        p_ik = model.U_matr[user_id][k]
        for user_id_, item_id, mark in marks:
            if user_id == user_id_:
                q_jk = model.V_matr[item_id][k]
                err += (mark - p_ik * q_jk) * (-q_jk)
        return err + self.reg * p_ik

    def d_vk(self, item_id, k, model, marks=None):
        marks = marks or self.train_marks
        err = 0
        q_jk = model.V_matr[item_id][k]
        for user_id, item_id_, mark in marks:
            if item_id == item_id_:
                p_ik = model.U_matr[user_id][k]
                err += (mark - p_ik * q_jk) * (-p_ik)
        return err + self.reg * q_jk

    def calc_matr_sqr_vals_sum(self, matr):
        return sum(sum(k ** 2 for k in vect) for vect in matr)

    def calc_loss_function(self, model, marks=None):
        marks = marks or self.train_marks
        sq_rmse = sum((r - model.predict(user_id, item_id)) ** 2
                      for user_id, item_id, r in marks) / len(marks)
        reg = self.reg * (
            self.calc_matr_sqr_vals_sum(
                model.U_matr.values()) / len(model.U_matr) +
            self.calc_matr_sqr_vals_sum(
                model.V_matr.values()) / len(model.V_matr))
        return 1. / 2 * (sq_rmse + reg)

    def train(self, model, marks):
        self.train_marks = marks

        cur_loss = float('inf')
        for epoch in xrange(self.max_epochs):
            self.LOGGER.info(
                'epoch {}: cur_loss {}'.format(epoch, cur_loss)
            )
            new_model = self.train_epoch(model)
            new_loss = self.calc_loss_function(new_model)

            dif = cur_loss - new_loss
            cur_loss = new_loss
            self.LOGGER.info(
                'new loss {}, dif {}'.format(new_loss, dif))
            if dif < 0:
                self.LOGGER.warning('dif < 0')
                break
            model = new_model
            if dif < self.acc:
                break
        return model

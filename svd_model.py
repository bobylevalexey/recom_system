# coding=utf-8
import functools
import json
import math
import random

from utils import dot_product


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

    def load(self, file_name):
        with open(file_name) as f:
            factors_num, U, V = json.load(f)
        self.factors_num = factors_num
        self.U_matr = {int(id_): vect for id_, vect in U.iteritems()}
        self.V_matr = {int(id_): vect for id_, vect in V.iteritems()}

    def dump(self, file_name):
        with open(file_name, 'w') as f:
            json.dump((self.factors_num, self.U_matr, self.V_matr), f)

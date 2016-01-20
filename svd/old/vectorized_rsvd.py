# coding=utf-8
from copy import deepcopy

import numpy as np
import time

from svd.base import BaseRSVD


def _dot_product(v1, v2):
    return sum(v1i * v2i for v1i, v2i in zip(v1, v2))


class VectorizedRSVD(BaseRSVD):
    def __init__(self, marks_list, lrate, reg, factors_num, max_epochs, acc):
        self.user_indexes = None
        self.item_indexes = None

        self.U_matr = None
        self.V_matr = None
        self.R_matr = None
        self.M_matr = None
        super(VectorizedRSVD, self).__init__(
                marks_list, lrate, reg, factors_num, max_epochs, acc)

    def init_user_and_item_indexes(self, marks):
        self.user_indexes = {}
        self.item_indexes = {}
        u_idx = i_idx = 0
        for user_id, item_id, mark in marks:
            if user_id not in self.user_indexes:
                self.user_indexes[user_id] = u_idx
                u_idx += 1
            if item_id not in self.item_indexes:
                self.item_indexes[item_id] = i_idx
                i_idx += 1

    def create_matr(self, n, m, init_val, dtype=None):
        matr = np.empty((n, m), dtype)
        matr.fill(init_val)
        return matr

    def init_model(self, marks):
        self.init_user_and_item_indexes(marks)

        self.U_matr = self.create_matr(
                len(self.user_indexes), self.factors_num, 0.5, float)
        self.V_matr = self.create_matr(
                len(self.item_indexes), self.factors_num, 0.5, float)
        self.R_matr = np.zeros((len(self.user_indexes), len(self.item_indexes)))
        self.M_matr = np.zeros((len(self.user_indexes), len(self.item_indexes)))

        for user_id, item_id, mark in marks:
            u_idx = self.user_indexes[user_id]
            i_idx = self.item_indexes[item_id]
            self.R_matr[u_idx, i_idx] = mark
            self.M_matr[u_idx, i_idx] = 1

    def predict(self, user_id, item_id):
        try:
            return np.dot(self.U_matr[self.user_indexes[user_id]],
                          self.V_matr[self.item_indexes[item_id]])
        except KeyError:
            pass

    def calc_model_rmse(self):
        return self.calc_rmse(self.R_matr)

    def calc_matr_sqr_vals_sum(self, matr):
        return sum(sum(k ** 2 for k in vect) for vect in matr)

    def calc_loss_function(self):
        sq_rmse = (self.R_matr - self.U_matr.dot(self.V_matr.transpose())) ** 2
        reg = self.reg * ((self.U_matr ** 2 + self.V_matr**2).sum())
        return 1./2 * (sq_rmse + reg)

    def d_U(self):
        a1 = - self.V_matr.transpose().dot(self.R_matr.transpose())
        a2 = (self.V_matr * self.V_matr).transpose().dot(
                self.M_matr.transpose()) * self.U_matr.transpose()
        a3 = self.reg * self.U_matr.transpose()
        return (a1 + a2 + a3).transpose()

    def d_V(self):
        a1 = - self.U_matr.transpose().dot(self.R_matr.transpose())
        a2 = (self.U_matr * self.U_matr).transpose().dot(
                self.M_matr.transpose()) * self.V_matr.transpose()
        a3 = self.reg * self.V_matr.transpose()
        return (a1 + a2 + a3).transpose()

    def train(self):
        cur_loss_func_val = 10000000
        for epoch_num in xrange(self.max_epochs):
            print 'epoch {}. cur loss - {}'.format(epoch_num + 1,
                                                   cur_loss_func_val)
            new_U_matr = self.U_matr - self.lrate * self.d_U()
            new_V_matr = self.V_matr - self.lrate * self.d_V()

            self.U_matr = new_U_matr
            self.V_matr = new_V_matr


            # for user_id, user_vect in self.U_matr.iteritems():
            #     new_user_vect = []
            #     for k, k_val in enumerate(user_vect):
            #         new_user_vect.append(k_val - self.lrate * self.d_u(
            #                 user_id, k))
            #     new_U_matr[user_id] = new_user_vect
            #
            # for item_id, item_vect in self.V_matr.iteritems():
            #     new_item_vect = []
            #     for k, k_val in enumerate(item_vect):
            #         new_item_vect.append(
            #                 k_val - self.lrate * self.d_v(item_id, k))
            #     new_V_matr[item_id] = new_item_vect
            # self.U_matr = new_U_matr
            # self.V_matr = new_V_matr

            new_loss_func_val = self.calc_loss_function()
            dif = cur_loss_func_val - new_loss_func_val
            cur_loss_func_val = new_loss_func_val
            print 'new loss - {}, dif - {}'.format(new_loss_func_val, dif)
            print
            if abs(dif) < self.acc:
                break


# R = [
#     (1, 1, 5),
#     (1, 2, 4),
#     (1, 3, 5),
#     (2, 1, 4),
#     (2, 3, 5),
#     (3, 2, 3),
#     (3, 3, 5),
#     (3, 5, 4),
#     (4, 4, 3),
#     (4, 5, 4),
#     (5, 3, 4),
#     (5, 4, 2),
#     (5, 5, 4),
#     (6, 1, 3),
#     (6, 6, 5)
# ]
#
# model = RSVD(R, 0.01, 1.25, 3, 100, 0.001)
# model.train()
# print model.calc_model_rmse()

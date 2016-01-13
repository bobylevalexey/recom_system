# coding=utf-8
from copy import deepcopy

from svd.base import BaseSVD


class StohasticRSVD(BaseSVD):
    # def find_min(self):
    def __init__(self, marks_list, lrate, reg, r, max_epochs, acc):
        self.U_matr = None
        self.V_matr = None
        self.R_matr = None
        super(StohasticRSVD, self).__init__(
                marks_list, lrate, reg, r, max_epochs, acc)

    def init_model(self, marks):
        self.U_matr = {}
        self.V_matr = {}
        self.R_matr = deepcopy(marks)

        for user_id, item_id, mark in marks:
            if user_id not in self.U_matr:
                # todo придумать умное начальное значение, а не 1
                self.U_matr[user_id] = [0.5] * self.r
            if item_id not in self.V_matr:
                # todo придумать умное начальное значение, а не 1
                self.V_matr[item_id] = [0.5] * self.r

    def train(self):
        for epoch in xrange(self.max_epochs):
            for k in xrange(self.r):
                denominator = sum(self.V_matr[i_id][k] ** 2
                                  for i_id in self.V_matr) + self.reg
                for user_id in self.U_matr:
                    self.U_matr[user_id][k] = sum(r * self.V_matr[i_id][k]
                                               for u_id, i_id, r in self.R_matr
                                               if u_id == user_id) / denominator
            for k in xrange(self.r):
                denominator = sum(self.U_matr[u_id][k] ** 2
                                  for u_id in self.U_matr) + self.reg
                for item_id in self.V_matr:
                    self.V_matr[item_id][k] = sum(r * self.U_matr[u_id][k]
                                               for u_id, i_id, r in self.R_matr
                                               if i_id == item_id) / denominator
            print self.calc_model_rmse()

    def calc_model_rmse(self):
        return self.calc_rmse(self.R_matr)

    def predict(self, user_id, item_id):
        if user_id not in self.U_matr or item_id not in self.V_matr:
            return
        return _dot_product(self.U_matr[user_id], self.V_matr[item_id])


def _dot_product(v1, v2):
    return sum(v1i * v2i for v1i, v2i in zip(v1, v2))


R = [
    (1, 1, 5),
    (1, 2, 4),
    (1, 3, 5),
    (2, 1, 4),
    (2, 3, 5),
    (3, 2, 3),
    (3, 3, 5),
    (3, 5, 4),
    (4, 4, 3),
    (4, 5, 4),
    (5, 3, 4),
    (5, 4, 2),
    (5, 5, 4),
    (6, 1, 3),
    (6, 6, 5)
]

model = StohasticRSVD(R, 0.01, 1.25, 3, 100, 0.001)
model.train()
print model.calc_model_rmse()

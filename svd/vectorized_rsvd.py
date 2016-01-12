# coding=utf-8
from copy import deepcopy

from base import BaseSVD


def _dot_product(v1, v2):
    return sum(v1i * v2i for v1i, v2i in zip(v1, v2))


class RSVD(BaseSVD):
    def __init__(self, marks_list, lrate, reg, r, max_epochs, acc):
        self.U_matr = None
        self.V_matr = None
        self.R_matr = None
        super(RSVD, self).__init__(
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

    def d_u(self, user_id, k):
        err = 0
        p_ik = self.U_matr[user_id][k]
        for user_id_, item_id, mark in self.R_matr:
            if user_id != user_id_:
                continue
            q_jk = self.V_matr[item_id][k]
            err += (mark - p_ik * q_jk) * (-q_jk)
        return err + self.reg * p_ik

    def predict(self, user_id, item_id):
        if user_id not in self.U_matr or item_id not in self.V_matr:
            return
        return _dot_product(self.U_matr[user_id], self.V_matr[item_id])

    def d_v(self, item_id, k):
        err = 0
        q_jk = self.V_matr[item_id][k]
        for user_id, item_id_, mark in self.R_matr:
            if item_id != item_id_:
                continue
            p_ik = self.U_matr[user_id][k]
            err += (mark - p_ik * q_jk) * (-p_ik)
        return err + self.reg * q_jk

    def calc_model_rmse(self):
        return self.calc_rmse(self.R_matr)

    def calc_matr_sqr_vals_sum(self, matr):
        return sum(sum(k ** 2 for k in vect) for vect in matr)

    def calc_loss_function(self):
        sq_rmse = sum((r - self.predict(user_id, item_id)) ** 2
                      for user_id, item_id, r in self.R_matr)
        reg = self.reg * (self.calc_matr_sqr_vals_sum(self.U_matr.values()) +
                          self.calc_matr_sqr_vals_sum(self.V_matr.values()))
        print sq_rmse, reg
        return 1./2 * (sq_rmse + reg)

    def train(self):
        cur_loss_func_val = 10000000
        for epoch_num in xrange(self.max_epochs):
            print 'epoch {}. cur loss - {}'.format(epoch_num + 1,
                                                   cur_loss_func_val)
            new_U_matr = {}
            new_V_matr = {}
            for user_id, user_vect in self.U_matr.iteritems():
                new_user_vect = []
                for k, k_val in enumerate(user_vect):
                    new_user_vect.append(k_val - self.lrate * self.d_u(
                            user_id, k))
                new_U_matr[user_id] = new_user_vect

            for item_id, item_vect in self.V_matr.iteritems():
                new_item_vect = []
                for k, k_val in enumerate(item_vect):
                    new_item_vect.append(
                            k_val - self.lrate * self.d_v(item_id, k))
                new_V_matr[item_id] = new_item_vect
            self.U_matr = new_U_matr
            self.V_matr = new_V_matr

            new_loss_func_val = self.calc_loss_function()
            print new_loss_func_val
            dif = cur_loss_func_val - new_loss_func_val
            cur_loss_func_val = new_loss_func_val
            print 'new loss - {}, dif - {}'.format(new_loss_func_val, dif)
            print
            if dif < self.acc:
                break


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

model = RSVD(R, 0.01, 1.25, 3, 100, 0.001)
model.train()
print model.calc_model_rmse()

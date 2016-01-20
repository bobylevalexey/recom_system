# coding=utf-8
import logging
import functools
from copy import deepcopy

from base import BaseRSVD, DictModel
from svd.utils import sqrt_avg_by_factors


class BruteRSVD(BaseRSVD):
    LOGGER = logging.getLogger('brute_rsvd')

    def train_epoch(self, model):
        """
        :param model: DictModel
        :param marks: (user_id, item_id, mark)
        """
        new_model = DictModel(model.factors_num)
        for user_id, user_vect in model.U_matr.iteritems():
            new_user_vect = []
            for k, k_val in enumerate(user_vect):
                new_user_vect.append(
                        k_val - self.lrate * self.d_uk(user_id, k, model))
            new_model.U_matr[user_id] = new_user_vect

        for item_id, item_vect in model.V_matr.iteritems():
            new_item_vect = []
            for k, k_val in enumerate(item_vect):
                new_item_vect.append(
                        k_val - self.lrate * self.d_vk(item_id, k, model))
            new_model.V_matr[item_id] = new_item_vect

        return new_model


class StohasticRSVD(BruteRSVD):
    def __init__(self, lrate, reg, max_epochs, acc, lrate_decr_coef,
                 max_fact_epochs):
        super(StohasticRSVD, self).__init__(lrate, reg, max_epochs, acc,
                                            lrate_decr_coef)
        self.max_fact_epochs = max_fact_epochs

    def train_epoch(self, model):
        for k in xrange(model.factors_num):
            model = self.train_k_factor(model, k)
        return model

    def train_k_factor(self, model, k):
        cur_loss = self.calc_loss_function(model)
        for fact_epoch in xrange(self.max_fact_epochs):
            self.LOGGER.info('factor {}: epoch {}: cur loss {}'.format(
                    k, fact_epoch, cur_loss))

            new_model = deepcopy(model)
            for user_id in model.U_matr:
                old_val = new_model.U_matr[user_id][k]
                new_model.U_matr[user_id][k] = \
                    old_val - self.lrate * self.d_uk(user_id, k, model)

            for item_id in model.V_matr:
                old_val = new_model.V_matr[item_id][k]
                new_model.V_matr[item_id][k] = \
                    old_val - self.lrate * self.d_vk(item_id, k, model)

            new_loss = self.calc_loss_function(new_model)
            dif = cur_loss - new_loss
            cur_loss = new_loss
            self.LOGGER.info(
                'new loss {}, dif {}'.format(new_loss, dif))
            if dif < 0:
                self.lrate *= self.lrate_decr_coef
                self.LOGGER.warning('{} factor: decreasing lrate'.format(k))
                continue
            model = new_model
            if dif < self.acc:
                break
        return model

if __name__ == "__main__":
    from svd.test_data import R
    logging.basicConfig(level=logging.INFO)

    svd = StohasticRSVD(lrate=0.001, reg=0, max_epochs=100,
                        acc=0.001, max_fact_epochs=400, lrate_decr_coef=0.4)
    # svd = BruteRSVD(lrate=0.01, reg=0.1, max_epochs=400,
    #                 acc=0.01)
    model = DictModel(2).with_val(1).init_from_marks_list(R)
            # sqrt_avg_by_factors(R, 2)).init_from_marks_list(R)

    new_model = svd.train(model, R)
    print new_model.calc_rmse(R), model.calc_rmse(R)



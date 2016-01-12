from abc import ABCMeta, abstractmethod
import math


class BaseSVD(object):
    __metaclass__ = ABCMeta

    def __init__(self, marks_list, lrate, reg, r, max_epochs, acc):
        self.lrate = lrate
        self.reg = reg
        self.r = r
        self.max_epochs = max_epochs
        self.acc = acc

        self.init_model(marks_list)

    @abstractmethod
    def init_model(self, marks):
        pass

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def predict(self, user_id, item_id):
        """
        returns None if user_id or item_id doesn't present in model
        :param user_id:
        :param item_id:
        """
        pass

    def calc_rmse(self, marks):
        sqr_err = 0
        marks_found = 0
        for user_id, item_id, mark in marks:
            predict = self.predict(user_id, item_id)
            if predict is not None:
                sqr_err += (mark - predict) ** 2
                marks_found += 1
        return math.sqrt(sqr_err / marks_found)

    @abstractmethod
    def calc_model_rmse(self):
        pass

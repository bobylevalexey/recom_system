
# Daniel Alabi and Cody Wang
# ======================================
# SvdMatrix:
# generates matrices U and V such that
# U * V^T closely approximates
# the original matrix (in this case, the utility
# matrix M)
# =======================================

import math


class Rating:
    """
    Rating class.
    Store every rating associated with a particular
    userid and movieid.
    ================Optimization======================
    """
    def __init__(self, userid, movieid, rating):
        self.uid = userid
        self.mid = movieid

        self.rat = rating


class SvdMatrix:
    def __init__(self, factors_num=30, lrate=0.035,
                 reg=0.01, max_epochs=30,
                 acc=0.001):
        """
        r_matr -> list of ratings (user_id, item_id, rating)
        nusers -> number of users in dataset
        nmovies -> number of movies in dataset
        r -> rank of approximation (for U and V)
        lrate -> learning rate
        regularizer -> regularizer
        """
        self.factors_num = factors_num
        self.lrate = lrate
        self.reg = reg
        self.acc = acc
        self.max_epochs = max_epochs

        # tmp variables
        self._train_marks = None
        self._train_model = None

    def train_k_factor(self, k):
        """
        Trains the kth column in U and the kth row in
        V^T
        See docs for more details.
        """
        sse = 0.0

        for user_id, item_id, mark in self._train_marks:
            err = mark - self._train_model.predict(user_id, item_id)
            sse += err**2

            old_pik = self._train_model.U_matr[user_id][k]
            old_qjk = self._train_model.V_matr[item_id][k]

            self._train_model.U_matr[user_id][k] += \
                self.lrate * (err * old_qjk - self.reg * old_pik)
            self._train_model.V_matr[item_id][k] += \
                self.lrate * (err * old_pik - self.reg * old_qjk)
        return math.sqrt(sse / len(self._train_marks))

    def train(self, model, marks):
        """
        Trains the entire U matrix and the entire V (and V^T) matrix
        """
        self._train_model = model
        self._train_marks = marks

        old_err = float('inf')
        for k in range(self.factors_num):
            print "k=", k
            for epoch in range(self.max_epochs):
                err = self.train_k_factor(k)

                # check if train error is still changing
                if abs(old_err - err) < self.acc:
                    break
                old_err = err
                print "epoch=", epoch, "; err=", err

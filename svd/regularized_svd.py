# Daniel Alabi and Cody Wang
# ======================================
# SvdMatrix:
# generates matrices U and V such that
# U * V^T closely approximates
# the original matrix (in this case, the utility
# matrix M)
# =======================================

import math
import time

from sklearn.cross_validation import train_test_split

from create_svd_input import get_marks_list_from_db
from model import connect


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
    def __init__(self, r_matr, n_users=None, n_items=None, r=30, l_rate=0.035,
                 regularizer=0.01, test_size=0.2, max_epochs=30,
                 accuracy=0.001):
        """
        r_matr -> list of ratings (user_id, item_id, rating)
        """
        self._user_ids = None
        self._item_ids = None
        self.train_set, self.test_set = train_test_split(
                self._ids_to_indexes(r_matr),
                test_size=test_size)

        self.n_users = n_users or len(self._user_ids)
        self.n_items = n_items or len(self._item_ids)

        # get average rating
        avg = self.averagerating()
        # set initial values in U, V using square root
        # of average/rank
        init_val = math.sqrt(avg/r)

        # U matrix
        self.U = [[init_val] * r for _ in range(self.n_users)]
        # V matrix -- easier to store and compute than V^T
        self.V = [[init_val] * r for _ in range(self.n_items)]

        self.r = r
        self.l_rate = l_rate
        self.regularizer = regularizer
        self.minimprov = accuracy
        self.maxepochs = max_epochs

    def _ids_to_indexes(self, rating_list):
        self._user_ids = {}
        self._item_ids = {}

        new_rating_list = []
        max_user_id = 0
        max_item_id = 0
        for user_id, item_id, rating in rating_list:
            if user_id not in self._user_ids:
                self._user_ids[user_id] = max_user_id
                max_user_id += 1
            if item_id not in self._item_ids:
                self._item_ids[item_id] = max_item_id
                max_item_id += 1
            new_rating_list.append(
                Rating(self._user_ids[user_id], self._item_ids[item_id],
                       rating))
        return new_rating_list

    def dotproduct(self, v1, v2):
        """
        Returns the dot product of v1 and v2
        """
        return sum([v1[i]*v2[i] for i in range(len(v1))])

    def calcrating(self, user_idx, item_idx):
        return self._predict_r_matr_cell(self._user_ids[user_idx],
                                         self._item_ids[item_idx])
        p = self.dotproduct(self.U[user_idx], self.V[item_idx])
        if p > 5:
            p = 5
        elif p < 1:
            p = 1
        return p

    def averagerating(self):
        """
        Returns the average rating of the entire dataset
        """
        avg = 0
        n = 0
        for i in range(len(self.train_set)):
            avg += self.train_set[i].rat
            n += 1
        return float(avg/n)

    def _predict_r_matr_cell(self, i, j):
        """
        Predicts the estimated rating for user with id i
        for movie with id j
        """
        p = self.dotproduct(self.U[i], self.V[j])
        if p > 5:
            p = 5
        elif p < 1:
            p = 1
        return p

    def train(self, k):
        """
        Trains the kth column in U and the kth row in
        V^T
        See docs for more details.
        """
        sse = 0.0
        n = 0
        for i in range(len(self.train_set)):
            # get current rating
            crating = self.train_set[i]
            err = crating.rat - self._predict_r_matr_cell(crating.uid, crating.mid)
            sse += err**2
            n += 1

            uTemp = self.U[crating.uid][k]
            vTemp = self.V[crating.mid][k]

            self.U[crating.uid][k] += self.l_rate * (err * vTemp - self.regularizer * uTemp)
            self.V[crating.mid][k] += self.l_rate * (err * uTemp - self.regularizer * vTemp)
        return math.sqrt(sse/n)

    def trainratings(self):
        """
        Trains the entire U matrix and the entire V (and V^T) matrix
        """
        # stub -- initial train error
        oldtrainerr = 1000000.0

        for k in range(self.r):
            for epoch in range(self.maxepochs):
                trainerr = self.train(k)

                # check if train error is still changing
                if abs(oldtrainerr-trainerr) < self.minimprov:
                    break
                oldtrainerr = trainerr

    def calcrmse(self, arr):
        """
        Calculates the RMSE using between arr
        and the estimated values in (U * V^T)
        """
        sse = 0.0
        total = 0
        for i in range(len(arr)):
            crating = arr[i]
            sse += (crating.rat - self.calcrating(crating.uid, crating.mid))**2
            total += 1
        return math.sqrt(sse/total)

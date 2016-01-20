
# Daniel Alabi and Cody Wang
# ======================================
# SvdMatrix:
# generates matrices U and V such that
# U * V^T closely approximates
# the original matrix (in this case, the utility
# matrix M)
# =======================================

import math

from sklearn.cross_validation import train_test_split

from svd.create_svd_input import get_marks_list_from_db
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
    def __init__(self, r_matr, nusers=None, nitems=None, r=30, lrate=0.035,
                 regularizer=0.01, test_size=0.2, max_epochs=30,
                 accuracy=0.001):
        """
        r_matr -> list of ratings (user_id, item_id, rating)
        nusers -> number of users in dataset
        nmovies -> number of movies in dataset
        r -> rank of approximation (for U and V)
        lrate -> learning rate
        regularizer -> regularizer
        """
        self._user_ids = None
        self._item_ids = None
        self.trainrats, self.testrats = train_test_split(
                self._ids_to_indexes(r_matr),
                test_size=test_size)

        self.nusers = nusers or len(self._user_ids)
        self.nitems = nitems or len(self._item_ids)

        # get average rating
        avg = self.averagerating()
        # set initial values in U, V using square root
        # of average/rank
        initval = math.sqrt(avg/r)

        # U matrix
        self.U = [[initval]*r for i in range(self.nusers)]
        # V matrix -- easier to store and compute than V^T
        self.V = [[initval] * r for i in range(self.nitems)]

        self.r = r
        self.lrate = lrate
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

    def calcrating(self, uid, mid):
        """
        Returns the estimated rating corresponding to userid for movieid
        Ensures returns rating is in range [1,5]
        """
        p = self.dotproduct(self.U[uid], self.V[mid])
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
        for i in range(len(self.trainrats)):
            avg += self.trainrats[i].rat
            n += 1
        return float(avg/n)

    def predict(self, i, j):
        """
        Predicts the estimated rating for user with id i
        for movie with id j
        """
        return self.calcrating(i, j)

    def train(self, k):
        """
        Trains the kth column in U and the kth row in
        V^T
        See docs for more details.
        """
        sse = 0.0
        n = 0
        for i in range(len(self.trainrats)):
            # get current rating
            crating = self.trainrats[i]
            err = crating.rat - self.predict(crating.uid, crating.mid)
            sse += err**2
            n += 1

            uTemp = self.U[crating.uid][k]
            vTemp = self.V[crating.mid][k]

            self.U[crating.uid][k] += self.lrate * (err*vTemp - self.regularizer*uTemp)
            self.V[crating.mid][k] += self.lrate * (err*uTemp - self.regularizer*vTemp)
        return math.sqrt(sse/n)

    def trainratings(self):
        """
        Trains the entire U matrix and the entire V (and V^T) matrix
        """
        # stub -- initial train error
        oldtrainerr = 1000000.0

        for k in range(self.r):
            # print "k=", k
            for epoch in range(self.maxepochs):
                trainerr = self.train(k)

                # check if train error is still changing
                if abs(oldtrainerr-trainerr) < self.minimprov:
                    break
                oldtrainerr = trainerr
                # print "epoch=", epoch, "; trainerr=", trainerr

    def calcrmse(self, arr):
        """
        Calculates the RMSE using between arr
        and the estimated values in (U * V^T)
        """
        nusers = self.nusers
        nmovies = self.nitems
        sse = 0.0
        total = 0
        for i in range(len(arr)):
            crating = arr[i]
            sse += (crating.rat - self.calcrating(crating.uid, crating.mid))**2
            total += 1
        return math.sqrt(sse/total)

    def readinratings(self, fname, arr, splitter="\t"):
        """
        Read in the ratings from fname and put in arr
        Use splitter as delimiter in fname
        """
        f = open(fname)

        for line in f:
            newline = [int(each) for each in line.split(splitter)]
            userid, movieid, rating = newline[0], newline[1], newline[2]
            arr.append(Rating(userid, movieid, rating))

        arr = sorted(arr, key=lambda rating: (rating.uid, rating.mid))
        return len(arr)

    def readtrainsmaller(self, fname):
        """
        Read in the smaller train dataset
        """
        return self.readinratings(fname, self.trainrats, splitter="\t")

    def readtrainlarger(self, fname):
        """
        Read in the large train dataset
        """
        return self.readinratings(fname, self.trainrats, splitter="::")

    def readtestsmaller(self, fname):
        """
        Read in the smaller test dataset
        """
        return self.readinratings(fname, self.testrats, splitter="\t")

    def readtestlarger(self, fname):
        """
        Read in the larger test dataset
        """
        return self.readinratings(fname, self.testrats, splitter="::")



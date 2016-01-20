import time

from model import connect
from svd.create_svd_input import get_marks_list_from_db
from svd.old.regularizedSVD import SvdMatrix

if __name__ == "__main__":
    #========= test SvdMatrix class on smallest MovieLENS dataset =========
    connect()
    r_matr = get_marks_list_from_db()

    results = []
    for i in xrange(1, 40):
        init = time.time()
        svd = SvdMatrix(r_matr, r=i)
        svd.trainratings()
        results.append((svd.calcrmse(svd.trainrats), svd.calcrmse(svd.testrats)))
        print "rmsetrain: ", results[-1][0]
        print "rmsetest: ", results[-1][1]
        print "time: ", time.time()-init
    for i in xrange(1, 100):
        print i, results[i]

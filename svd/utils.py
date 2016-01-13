import time

from svd.regularizedSVD import SvdMatrix


def run_svd(data, r, regularizer, accuracy, test_size=0.3, verbose=True):
    init_time = time.time()
    svd = SvdMatrix(data, r=r, regularizer=regularizer, test_size=test_size,
                    max_epochs=200, accuracy=accuracy)
    svd.trainratings()
    train_rmse, test_rmse = svd.calcrmse(svd.trainrats),\
                            svd.calcrmse(svd.testrats)
    if verbose:
        print (
            "Results of SVD(r={r}, regularizer={reg}, accuracy={acc}, "
            "test_size={ts})\n"
            "rmse train: {tr_rmse}\n"
            "rmse test:  {test_rmse}\n"
            "time:       {time}".format(
                tr_rmse=train_rmse, test_rmse=test_rmse,
                time=time.time() - init_time,
                r=r, reg=regularizer, acc=accuracy, ts=test_size
            )
        )
    return {
        "train_rmse": train_rmse, "test_rmse": test_rmse, "svd": svd
    }

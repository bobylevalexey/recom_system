import os
import pickle

import rs_config
from create_svd_input import get_marks_list_from_db
from model import connect
from svd.base import DictModel
# from svd.utils import run_svd




# factor_num_choices = xrange(5, 16)
# reg_choices = frange(0.01, 1., 0.05)
# lrate_choices = frange(0.01, 1., 0.05)
# model_choices = []
# print len(list(reg_choices))
# reg_choices = [0.0025, 0.005, 0.001, 0.025, 0.05, 0.1, 0.2, 0.4, 0.8]
# acc_choices = [0.0025, 0.005, 0.001, 0.025, 0.05, 0.1, 0.2, 0.4, 0.8]

# if __name__ == "__main__ ":
#     connect()
#     r_matr = get_marks_list_from_db()
#     results = []
#     for r in r_choices:
#         for reg in reg_choices:
#             for acc in acc_choices:
#                 res = run_svd(r_matr, r, reg, acc)
#                 res.update(dict(r=r, reg=reg, acc=acc))
#                 results.append(res)
#                 print res
#     with open(os.path.join(
#             rs_config.DATA_DIR, 'params_test_results.pickle'), 'w') as f:
#         pickle.dump(results, f)

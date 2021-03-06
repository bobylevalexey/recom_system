import math
from datetime import date
from itertools import product

import numpy as np


def marks_avg(marks):
    return float(sum(mark for uid, iid, mark in marks)) / len(marks)


def sqrt_by_factors(val, factors_num):
    math.sqrt(val / factors_num)


def sqrt_avg_by_factors(marks, factors_num):
    return sqrt_by_factors(marks_avg(marks), factors_num)


def dot_product(v1, v2):
    return sum(v1i * v2i for v1i, v2i in zip(v1, v2))


def frange(x, y, jump):
    while x <= y:
        yield x
        x += jump


def replace_nones(matr, val):
    for i, j in product(xrange(matr.shape[0]), xrange(matr.shape[1])):
        if np.isnan(matr[i, j]):
            matr[i, j] = val
    return matr


def get_age(born, init_date=None):
    init_date = init_date or date(year=2016, month=1, day=1)
    return init_date.year - born.year - \
           ((init_date.month, init_date.day) < (born.month, born.day))


def get_marks_counts(marks_list, by_items=False):
    ids_idx = bool(by_items)  # marks_list = [(u_id, i_id, mark), ...]
                              # so by_items==True, we select i_id else u_id
    marks_counts = {}
    for m_tup in marks_list:
        id_ = m_tup[ids_idx]
        marks_counts[id_] = marks_counts.get(id_, 0) + 1
    return marks_counts

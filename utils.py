import math
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
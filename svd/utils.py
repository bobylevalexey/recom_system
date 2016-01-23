import math


def marks_avg(marks):
    return float(sum(mark for uid, iid, mark in marks)) / len(marks)


def sqrt_avg_by_factors(marks, factros_num):
    return math.sqrt(marks_avg(marks) / factros_num)


def dot_product(v1, v2):
    return sum(v1i * v2i for v1i, v2i in zip(v1, v2))


def frange(x, y, jump):
    while x <= y:
        yield x
        x += jump

import csv

import numpy as np
from rsvd import rating_t
from sklearn.cross_validation import train_test_split

import rs_config
from model import connect, session_scope
from tables import FlampMarksTable, FoodEkbFirms


def get_marks_list_from_db():
    with session_scope() as sess:
        return sess.query(
                FlampMarksTable.firm_id, FlampMarksTable.expert_id,
                FlampMarksTable.mark
        ).join(
                FoodEkbFirms, FoodEkbFirms.food_pk == FlampMarksTable.firm_id
        ).all()


def save_as_csv(marks_list):
    train_writer = csv.writer(rs_config.SVD_TRAIN_SET_CSV_FILE, delimeter=',')
    test_writer = csv.writer(rs_config.SVD_TEST_SET_CSV_FILE)


if __name__ == "__main__":
    connect()
    R_matrix = np.asarray(get_marks_list_from_db(), dtype=rating_t)
    train, test = train_test_split(R_matrix, test_size=0.2)
    train.tofile(rs_config.SVD_TRAIN_SET_FILE)
    test.tofile(rs_config.SVD_TEST_SET_FILE)

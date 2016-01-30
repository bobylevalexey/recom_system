import os

from rs_config import DATA_DIR

ML_DATA_DIR = os.path.join(DATA_DIR, 'movielens_data')

RSVD_OPTIONS = dict(
    lrate=0.009,
    acc=1,
    reg=0.1,
    max_epochs=5000,
    deep_copy=True,
    glob_epochs=1,
)

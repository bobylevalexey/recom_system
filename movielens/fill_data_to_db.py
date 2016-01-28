import os
from datetime import datetime

import functools

from model import connect, session_scope
from movielens.ml_tables import MLUsers, MLMovies, MLMarks
from rs_config import DATA_DIR

sex_dict = {
    'F': 'female',
    'M': 'male'
}


USER_COLS_AND_FUNCS = [
    ('id_', int),
    ('age', int),
    ('sex', sex_dict.get),
    ('occupation', lambda x: x),
    ('zip_code', lambda x: x)
]


def to_bool(int_str):
    return bool(int(int_str))

to_unicode = functools.partial(unicode, errors='ignore')


def to_date(date_str):
    if date_str != '':
        return datetime.strptime(date_str, '%d-%b-%Y').date()


MOVIE_COLS_AND_FUNCS = [
    ('id_', int),
    ('name', to_unicode),
    ('release_date', to_date),
    ('video_release_date', to_date),
    ('imdb_url', to_unicode),
    ('is_unknown', to_bool),
    ('is_action', to_bool),
    ('is_adventure', to_bool),
    ('is_animation', to_bool),
    ('is_for_children', to_bool),
    ('is_comedy', to_bool),
    ('is_crime', to_bool),
    ('is_documentary', to_bool),
    ('is_drama', to_bool),
    ('is_fantasy', to_bool),
    ('is_film_noir', to_bool),
    ('is_horror', to_bool),
    ('is_musical', to_bool),
    ('is_mystery', to_bool),
    ('is_romance', to_bool),
    ('is_sci_fi', to_bool),
    ('is_thriller', to_bool),
    ('is_war', to_bool),
    ('is_western', to_bool),
]

MARK_COLS_AND_FUNCS = [
    ('user_id', int),
    ('movie_id', int),
    ('mark', int),
    ('data', int),
]


def load_to_table(table, columns_and_funcs, file_name, sep='|'):
    with open(file_name) as f:
        data_lines = f.readlines()
    with session_scope() as sess:
        for data_line in data_lines:
            data_line = data_line.rstrip()
            data_line_items = data_line.split(sep)
            table_row = {}
            print data_line_items
            for item, col_and_func in zip(data_line_items, columns_and_funcs):
                col, func = col_and_func
                table_row[col] = func(item)
            sess.add(table(**table_row))


if __name__ == "__main__":
    to_date('26-Apr-1986')
    connect()

    ml_data_dir = os.path.join(DATA_DIR, 'movielens_data')

    load_to_table(MLUsers, USER_COLS_AND_FUNCS,
                  os.path.join(ml_data_dir, 'users'))
    load_to_table(MLMovies, MOVIE_COLS_AND_FUNCS,
                  os.path.join(ml_data_dir, 'movies'))
    load_to_table(MLMarks, MARK_COLS_AND_FUNCS,
                  os.path.join(ml_data_dir, 'marks'), sep='\t')


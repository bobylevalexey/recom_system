import os

from sklearn.cross_validation import train_test_split

from model import connect
from regressions import LogisticModel
from svd_model import DictModel
from movielens.config import ML_DATA_DIR
from movielens.get_features import get_movies_features

GENRES = [
    'unknown', 'action', 'adventure', 'animation', 'for_children', 'comedy',
    'crime', 'documentary', 'drama', 'fantasy', 'film_noir', 'horror',
    'musical', 'mystery', 'romance', 'sci_fi', 'thriller', 'war', 'western'
]


def check_genre(svd, features, genre):
    feature_name = 'is_' + genre
    genre_dict = {id_: int(dict_[feature_name])
                  for id_, dict_ in get_movies_features().iteritems()
                  if dict_[feature_name] is not None}

    l = LogisticModel()
    train_ids, test_ids = train_test_split(genre_dict.keys(), train_size=0.7)
    print l.train(ml_model.V_matr, genre_dict, train_ids)
    print l.get_err_from_dicts(ml_model.V_matr, genre_dict, test_ids)

if __name__ == "__main__":
    connect()
    ml_model = DictModel()
    ml_model.load(os.path.join(ML_DATA_DIR, 'model.json'))
    features = get_movies_features()

    for genre in GENRES:
        print
        print '----------'
        print genre
        check_genre(ml_model, features, genre)



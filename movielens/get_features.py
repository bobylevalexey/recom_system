from datetime import date

from model import get_dict
from movielens.ml_tables import MLUsers, MLMovies
from utils import get_age


def _get_features_dict(table, columns):
    f_dict = {}
    for row_dict in get_dict(table, columns + ['id_']):
        id_ = row_dict.pop('id_')
        f_dict[id_] = row_dict
    return f_dict


def get_users_features():
    return _get_features_dict(MLUsers, ['age', 'occupation', 'sex'])


def get_movies_features():
    columns = [
        'release_date', 'is_unknown', 'is_action', 'is_adventure',
        'is_animation', 'is_for_children', 'is_comedy', 'is_crime',
        'is_documentary', 'is_drama', 'is_fantasy', 'is_film_noir', 'is_horror',
        'is_musical', 'is_mystery', 'is_romance', 'is_sci_fi', 'is_thriller',
        'is_war', 'is_western'
    ]
    movies_features = _get_features_dict(MLMovies, columns)
    for m_dict in movies_features.values():
        try:
            m_dict['age'] = get_age(m_dict.pop('release_date'),
                                    date(2000, 1, 1))
        except AttributeError:
            m_dict['age'] = None
        for key in m_dict.keys():
            if key.startswith('is_'):
                m_dict[key] = int(m_dict[key])
    return movies_features

if __name__ == "__main__":
    from model import connect

    connect()
    print get_movies_features()

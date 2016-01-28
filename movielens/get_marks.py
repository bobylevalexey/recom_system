from model import get
from movielens.ml_tables import MLMarks


def get_ml_marks():
    return [(m.user_id, m.movie_id, m.mark)
            for m in get(MLMarks, {}, all_=True)]

if __name__ == "__main__":
    from model import connect

    connect()
    print get_ml_marks()[:10]


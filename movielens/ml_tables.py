import sqlalchemy as sa

from model import Base


class MLUsers(Base):
    __tablename__ = 'ml_users'

    id_ = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    sex = sa.Column(sa.Text)
    occupation = sa.Column(sa.Text)
    zip_code = sa.Column(sa.Text)


class MLMovies(Base):
    __tablename__ = 'ml_movies'

    id_ = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text)
    release_date = sa.Column(sa.Date)
    video_release_date = sa.Column(sa.Date)
    imdb_url = sa.Column(sa.Text)

    # genres
    is_unknown = sa.Column(sa.Boolean)
    is_action = sa.Column(sa.Boolean)
    is_adventure = sa.Column(sa.Boolean)
    is_animation = sa.Column(sa.Boolean)
    is_for_children = sa.Column(sa.Boolean)
    is_comedy = sa.Column(sa.Boolean)
    is_crime = sa.Column(sa.Boolean)
    is_documentary = sa.Column(sa.Boolean)
    is_drama = sa.Column(sa.Boolean)
    is_fantasy = sa.Column(sa.Boolean)
    is_film_noir = sa.Column(sa.Boolean)
    is_horror = sa.Column(sa.Boolean)
    is_musical = sa.Column(sa.Boolean)
    is_mystery = sa.Column(sa.Boolean)
    is_romance = sa.Column(sa.Boolean)
    is_sci_fi = sa.Column(sa.Boolean)
    is_thriller = sa.Column(sa.Boolean)
    is_war = sa.Column(sa.Boolean)
    is_western = sa.Column(sa.Boolean)


class MLMarks(Base):
    __tablename__ = 'ml_marks'

    id_ = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.Integer)
    movie_id = sa.Column(sa.Integer)
    mark = sa.Column(sa.Integer)
    data = sa.Column(sa.Integer)  # timestamp

# coding=utf-8
from datetime import date

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
Session = sessionmaker(expire_on_commit=False)


class VkInfoTable(Base):
    __tablename__ = 'vk_info'
    id_ = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    vk_json = sqlalchemy.Column(sqlalchemy.Text)
    vk_id = sqlalchemy.Column(sqlalchemy.Text)

def _get_age(born):
    init_date = date(year=2016, month=1, day=1)
    return init_date.year - born.year - \
           ((init_date.month, init_date.day) < (born.month, born.day))


class VkFeatures(Base):
    __tablename__ = 'vk_features'

    SEX = {
        1: 'female',  # женский;
        2: 'male',  # мужской;
        0: 'undef',  # пол не указан.
    }
    RELATION = {
        1: 'not',  # не женат/не замужем
        2: 'has (boy|girl)friend',  # есть друг/есть подруга
        3: 'engaged',  # помолвлен/помолвлена
        4: 'married',  # женат/замужем
        5: 'difficult',  # всё сложно
        6: 'actively looking',  # в активном поиске
        7: 'in love',  # влюблён/влюблена
        0: 'undef',  # не указано
    }
    ALCO = {
        1: 'very negative',  # резко негативное
        2: 'negative',  # негативное
        3: 'neutral',  # нейтральное
        4: 'compromise',  # компромиссное
        5: 'positive',  # положительное
    }
    SMOKE = {
        1: 'very negative',  # резко негативное
        2: 'negative',  # негативное
        3: 'neutral',  # нейтральное
        4: 'compromise',  # компромиссное
        5: 'positive',  # положительное
    }
    POLIT = {
        1: 'communistic',  # коммунистические
        2: 'socialistic',  # социалистические
        3: 'moderate',  # умеренные
        4: 'liberal',  # либеральные
        5: 'conservative',  # консервативные
        6: 'monarchical',  # монархические
        7: 'ultraconservative',  # ультраконсервативные
        8: 'apathetic',  # индифферентные
        9: 'libertarian',  # либертарианские
    }
    PEOPLE_MAIN = {
        1: 'intelligence and creativity',  # ум и креативность
        2: 'kindness and honesty',  # доброта и честность
        3: 'beauty and health',  # красота и здоровье
        4: 'power and wealth',  # власть и богатство
        5: 'courage and perseverance',  # смелость и упорство
        6: 'Humor and love for life',  # юмор и жизнелюбие
    }
    LIFE_MAIN = {
        1: 'family and children',  # семья и дети
        2: 'career and money',  # карьера и деньги
        3: 'activities',  # развлечения и отдых
        4: 'science and research',  # наука и исследования
        5: 'improving the world',  # совершенствование мира
        6: 'self-development',  # саморазвитие
        7: 'beauty and art',  # красота и искусство
        8: 'fame and influence',  # слава и влияние
    }

    id_ = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    # general
    sex = sqlalchemy.Column(sqlalchemy.Integer)
    age = sqlalchemy.Column(sqlalchemy.Integer)
    bdate = sqlalchemy.Column(sqlalchemy.Date)
    relation = sqlalchemy.Column(sqlalchemy.Text)
    occupation_type = sqlalchemy.Column(sqlalchemy.Text)

    # counts
    albums_count = sqlalchemy.Column(sqlalchemy.Integer)
    videos_count = sqlalchemy.Column(sqlalchemy.Integer)
    audios_count = sqlalchemy.Column(sqlalchemy.Integer)
    photos_count = sqlalchemy.Column(sqlalchemy.Integer)
    friends_count = sqlalchemy.Column(sqlalchemy.Integer)
    groups_count = sqlalchemy.Column(sqlalchemy.Integer)
    pages_count = sqlalchemy.Column(sqlalchemy.Integer)
    followers_count = sqlalchemy.Column(sqlalchemy.Integer)
    user_videos_count = sqlalchemy.Column(sqlalchemy.Integer)
    notes_count = sqlalchemy.Column(sqlalchemy.Integer)
    user_photos_count = sqlalchemy.Column(sqlalchemy.Integer)
    subscriptions_count = sqlalchemy.Column(sqlalchemy.Integer)
    gifts_count = sqlalchemy.Column(sqlalchemy.Integer)

    # views
    political = sqlalchemy.Column(sqlalchemy.Text)
    people_main = sqlalchemy.Column(sqlalchemy.Text)
    life_main = sqlalchemy.Column(sqlalchemy.Text)
    smoking = sqlalchemy.Column(sqlalchemy.Text)
    alcohol = sqlalchemy.Column(sqlalchemy.Text)

    # security
    wall_comments = sqlalchemy.Column(sqlalchemy.Boolean)
    can_post = sqlalchemy.Column(sqlalchemy.Boolean)
    can_see_all_posts = sqlalchemy.Column(sqlalchemy.Boolean)
    can_see_audio = sqlalchemy.Column(sqlalchemy.Boolean)
    can_write_private_message = sqlalchemy.Column(sqlalchemy.Boolean)
    can_send_friend_request = sqlalchemy.Column(sqlalchemy.Boolean)

    # verbose
    activities = sqlalchemy.Column(sqlalchemy.Text)
    interests = sqlalchemy.Column(sqlalchemy.Text)
    music = sqlalchemy.Column(sqlalchemy.Text)
    movies = sqlalchemy.Column(sqlalchemy.Text)
    tv = sqlalchemy.Column(sqlalchemy.Text)
    books = sqlalchemy.Column(sqlalchemy.Text)
    games = sqlalchemy.Column(sqlalchemy.Text)
    about = sqlalchemy.Column(sqlalchemy.Text)
    quotes = sqlalchemy.Column(sqlalchemy.Text)

    def __init__(
            self, id_=None, sex=None, bdate=None, relation=None,
            occupation_type=None, albums_count=None, videos_count=None,
            audios_count=None, photos_count=None, friends_count=None,
            groups_count=None, pages_count=None, followers_count=None,
            user_videos_count=None, notes_count=None, user_photos_count=None,
            subscriptions_count=None, gifts_count=None, political=None,
            people_main=None, life_main=None, smoking=None, alcohol=None,
            wall_comments=None, can_post=None, can_see_all_posts=None,
            can_see_audio=None, can_write_private_message=None,
            can_send_friend_request=None, activities=None, interests=None,
            music=None, movies=None, tv=None, books=None, games=None,
            about=None, quotes=None):
        self.id_ = id_
        self.sex = self.SEX.get(sex)
        self.age = _get_age(bdate) if bdate is not None else None
        self.bdate = bdate
        self.relation = self.RELATION.get(relation)
        self.occupation_type = occupation_type
        self.albums_count = albums_count
        self.videos_count = videos_count
        self.audios_count = audios_count
        self.photos_count = photos_count
        self.friends_count = friends_count
        self.groups_count = groups_count
        self.pages_count = pages_count
        self.followers_count = followers_count
        self.user_videos_count = user_videos_count
        self.notes_count = notes_count
        self.user_photos_count = user_photos_count
        self.subscriptions_count = subscriptions_count
        self.gifts_count = gifts_count
        self.political = self.POLIT.get(political)
        self.people_main = self.PEOPLE_MAIN.get(people_main)
        self.life_main = self.LIFE_MAIN.get(life_main)
        self.smoking = self.SMOKE.get(smoking)
        self.alcohol = self.ALCO.get(alcohol)
        self.wall_comments = wall_comments
        self.can_post = can_post
        self.can_see_all_posts = can_see_all_posts
        self.can_see_audio = can_see_audio
        self.can_write_private_message = can_write_private_message
        self.can_send_friend_request = can_send_friend_request
        self.activities = activities
        self.interests = interests
        self.music = music
        self.movies = movies
        self.tv = tv
        self.books = books
        self.games = games
        self.about = about
        self.quotes = quotes


class FlampExpertsTable(Base):
    __tablename__ = 'flamp_experts'
    id_ = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                            autoincrement=True)
    flamp_url = sqlalchemy.Column(sqlalchemy.Text)
    vk_url = sqlalchemy.Column(sqlalchemy.Text)
    page = sqlalchemy.Column(sqlalchemy.Text)
    user_name = sqlalchemy.Column(sqlalchemy.Text)
    reviews = sqlalchemy.Column(sqlalchemy.Integer())


class FlampFirmsTable(Base):
    __tablename__ = 'flamp_firms'

    id_ = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                            autoincrement=True)
    flamp_id = sqlalchemy.Column(sqlalchemy.Text)
    page = sqlalchemy.Column(sqlalchemy.Text)
    category_url = sqlalchemy.Column(sqlalchemy.Text)
    is_food = sqlalchemy.Column(sqlalchemy.Integer)
    city = sqlalchemy.Column(sqlalchemy.Text)


class FlampMarksTable(Base):
    __tablename__ = 'flamp_marks'

    id_ = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                            autoincrement=True)
    expert_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey(FlampExpertsTable.id_))
    firm_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey(FlampFirmsTable.id_))
    mark = sqlalchemy.Column(sqlalchemy.Integer)
    mark_url = sqlalchemy.Column(sqlalchemy.Text)


class FoodEkbFirms(Base):
    __tablename__ = 'food_ekb_firms'

    food_pk = sqlalchemy.Column(sqlalchemy.ForeignKey(FlampFirmsTable.id_),
                                primary_key=True)

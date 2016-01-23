# coding=utf-8
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


class VkFeatures(Base):
    __tablename__ = 'vk_features'

    SEX = {
        1: 'fem',  # женский;
        2: 'male',  # мужской;
        0: 'undef',  # пол не указан.
    }
    RELATION = {
        1: 'not',  # не женат/не замужем
        2: 'friend',  # есть друг/есть подруга
        3: 'pomol',  # помолвлен/помолвлена
        4: 'zhen',  # женат/замужем
        5: 'slozh',  # всё сложно
        6: 'akt',  # в активном поиске
        7: 'vlub',  # влюблён/влюблена
        0: 'ne uk',  # не указано
    }
    ALCO = {
        1: 'rezk',  # резко негативное
        2: 'neg',  # негативное
        3: 'neut',  # нейтральное
        4: 'comp',  # компромиссное
        5: 'pol',  # положительное
    }
    SMOKE = {
        1: 'rezk',  # резко негативное
        2: 'neg',  # негативное
        3: 'neut',  # нейтральное
        4: 'comp',  # компромиссное
        5: 'pol',  # положительное
    }
    POLIT = {
        1: 'kom',  # коммунистические
        2: 'soc',  # социалистические
        3: 'umer',  # умеренные
        4: 'lib',  # либеральные
        5: 'kons',  # консервативные
        6: 'mon',  # монархические
        7: 'ult',  # ультраконсервативные
        8: 'ind',  # индифферентные
        9: 'libertar',  # либертарианские
    }
    PEOPLE_MAIN = {
        1: 'um',  # ум и креативность
        2: 'dob',  # доброта и честность
        3: 'kras',  # красота и здоровье
        4: 'vlast',  # власть и богатство
        5: 'cmel',  # смелость и упорство
        6: 'umor',  # юмор и жизнелюбие
    }
    LIFE_MAIN = {
        1: 'sem',  # семья и дети
        2: 'kar',  # карьера и деньги
        3: 'rasvl',  # развлечения и отдых
        4: 'nauka',  # наука и исследования
        5: 'sov mira',  # совершенствование мира
        6: 'samorazv',  # саморазвитие
        7: 'kras',  # красота и искусство
        8: 'slav',  # слава и влияние
    }

    id_ = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    # general
    sex = sqlalchemy.Column(sqlalchemy.Integer)
    bdate = sqlalchemy.Column(sqlalchemy.Date)
    relation = sqlalchemy.Column(sqlalchemy.Integer)
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
    political = sqlalchemy.Column(sqlalchemy.Integer)
    people_main = sqlalchemy.Column(sqlalchemy.Integer)
    life_main = sqlalchemy.Column(sqlalchemy.Integer)
    smoking = sqlalchemy.Column(sqlalchemy.Integer)
    alcohol = sqlalchemy.Column(sqlalchemy.Integer)

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

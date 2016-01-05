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

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

    def __init__(self, id_, flamp_url, vk_url, page, user_name, reviews):
        self.id_ = id_
        self.flamp_url = flamp_url
        self.vk_url = vk_url
        self.page = page
        self.user_name = user_name
        self.reviews = reviews


class FlampFirmsTable(Base):
    __tablename__ = 'flamp_firms'

    id_ = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                            autoincrement=True)
    flamp_id = sqlalchemy.Column(sqlalchemy.Text)
    page = sqlalchemy.Column(sqlalchemy.Text)
    category_url = sqlalchemy.Column(sqlalchemy.Text)

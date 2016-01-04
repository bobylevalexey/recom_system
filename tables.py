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

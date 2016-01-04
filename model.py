# coding=utf-8
import os
from contextlib import contextmanager

import sqlalchemy
from sqlalchemy.sql.elements import and_

from tables import Base, Session, FlampExpertsTable

DB_FILE = os.path.join(os.path.dirname(__file__), 'data', 'db.sqlite')


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def connect():
    engine = sqlalchemy.create_engine('sqlite:///' + DB_FILE)
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)


def insert(table, **kwargs):
    with session_scope() as sess:
        sess.add(table(**kwargs))


def get(table, all_=False, **filter_kwargs):
    filter_clause = and_(*[getattr(table, col_name) == val
                           for col_name, val in filter_kwargs.iteritems()])
    with session_scope() as sess:
        query = sess.query(table).filter(filter_clause)
        if all_:
            return query.all()
        else:
            return query.first()


class Storage(object):
    _DB_FILE = os.path.join(os.path.dirname(__file__), 'data', 'db.sqlite')

    def __init__(self):
        self._engine = None

    def connect(self):
        self._engine = sqlalchemy.create_engine('sqlite:///' + self._DB_FILE)
        Session.configure(bind=self._engine)
        Base.metadata.create_all(self._engine)

    def fill_expert(self, user_name, user_link, reviews, vk_link, user_page):
        with session_scope() as sess:
            sess.add(FlampExpertsTable(flamp_url=user_link, vk_url=vk_link,
                                       page=user_page, user_name=user_name, reviews=reviews))

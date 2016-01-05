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


def insert(table, **attrs):
    with session_scope() as sess:
        sess.add(table(**attrs))


def _get_filter_clause(table, filter_kwargs):
    return and_(*[getattr(table, col_name) == val
                  for col_name, val in filter_kwargs.iteritems()])


def _get_filtered_query(session, table, filter_kwargs):
    return session.query(table).filter(_get_filter_clause(table, filter_kwargs))


def get(table, filter_kwargs, all_=False):
    with session_scope() as sess:
        query = _get_filtered_query(sess, table, filter_kwargs)
        if all_:
            return query.all()
        else:
            return query.first()


def update(table, filter_kwargs, new_kwargs):
    with session_scope() as sess:
        updating_obj = _get_filtered_query(sess, table, filter_kwargs).one()
        for col, val in new_kwargs.iteritems():
            setattr(updating_obj, col, val)


def delete(table, filter_kwargs):
    with session_scope() as sess:
        _get_filtered_query(sess, table, filter_kwargs).delete()


def iterate_over_table(table, pk_col='id_'):
    with session_scope() as sess:
        pk_list = [tup[0] for tup in sess.query(getattr(table, pk_col)).all()]
    for pk in pk_list:
        yield get(table, {pk_col: pk})


if __name__ == "__main__":
    connect()
    # delete(FlampExpertsTable, {'id_': 1})

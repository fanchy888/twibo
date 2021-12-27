import traceback
from datetime import datetime
from contextlib import contextmanager
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, DateTime
from sqlalchemy import create_engine

from twibo_server.config import config

session_cache = {}
Base = declarative_base()


def get_session(name='default'):
    if name not in session_cache:
        engine = create_engine(config.sqldb_url, pool_size=20, pool_recycle=3600)
        session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        session_cache[name] = session

    session_class = session_cache[name]
    session_class()
    return session_class


def clear_session():

    for k in session_cache:
        try:
            session_cache[k].remove()
        except:
            traceback.print_exc()


@contextmanager
def session_manager():
    session = get_session()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


class MixinBase:
    create_time = Column(DateTime, default=datetime.utcnow)
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        with session_manager() as session:
            session.add(self)
            session.commit()


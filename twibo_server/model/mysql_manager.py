from datetime import datetime
from contextlib import contextmanager
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, DateTime
from twibo_server import engine


Session = sessionmaker(bind=engine)
Base = declarative_base()


class MixinBase:
    create_time = Column(DateTime, default=datetime.utcnow)
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


@contextmanager
def session_manager():
    session = Session()
    try:
        yield session
        session.commit()
    except :
        session.rollback()
        raise
    finally:
        session.close()


from datetime import datetime
from contextlib import contextmanager
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, DateTime
from twibo_server import engine


Session = sessionmaker(bind=engine)
Base = declarative_base()


@contextmanager
def session_manager():
    session = Session()
    try:
        yield session
        # session.commit()
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


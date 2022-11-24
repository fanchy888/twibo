from twibo_server.model.group import Base
from sqlalchemy import create_engine
from twibo_server.config import config


def create_table():
    engine = create_engine(config.sqldb_url)
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    create_table()
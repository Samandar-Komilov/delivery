from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session


engine = create_engine("postgresql://postgres:voidpostgres!@localhost/delivery_db", echo=True)

Base = declarative_base()
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
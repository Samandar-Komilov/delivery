from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine("postgresql://postgres:voidpostgres!@localhost/delivery_db", echo=True)

Base = declarative_base()
session = sessionmaker()



def init_db():
    Base.metadata.create_all(bind=engine)
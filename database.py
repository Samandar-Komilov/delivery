from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

import os
from dotenv import load_dotenv
load_dotenv()

DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_NAME=os.getenv("DB_NAME")


engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}/@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True)


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
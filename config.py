import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()


class Config:
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite:///digests.db"
    ENGINE = create_engine(SQLALCHEMY_DATABASE_URI)


# Create the SQLAlchemy engine and session
def create_session():
    Session = sessionmaker(bind=Config.ENGINE)
    session = Session()
    return session

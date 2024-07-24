from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQALCHEMY_DATABASE_URL = 'postgresql://postgres:nescafe@localhost/TodoApplicationDatabase'

engine = create_engine(SQALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


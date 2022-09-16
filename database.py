from click import echo
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db_credential import db

POSTGRE_DATABASE_URL = db.get('POSTGRE_DATABASE_URL')

engine=create_engine(POSTGRE_DATABASE_URL, echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
import databases
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from os import environ


DATABASE_URL = 'postgresql://{}:{}@{}/{}'.format(
    environ.get('POSTGRES_USER'),
    environ.get('POSTGRES_PASSWORD'),
    environ.get('POSTGRES_HOST'),
    environ.get('POSTGRES_DB')
)

db = databases.Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL)
metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

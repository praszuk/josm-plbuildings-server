from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from os import environ


DATABASE_URL = 'postgresql://{}:{}@{}/{}'.format(
    environ.get('POSTGRES_USER'),
    environ.get('POSTGRES_PASSWORD'),
    environ.get('POSTGRES_HOST'),
    environ.get('POSTGRES_DB')
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

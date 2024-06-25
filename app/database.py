from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import os

Base = declarative_base()
database_url = os.getenv('DATABASE_URL')
engine = create_engine(database_url.replace("postgres://", "postgresql://"), echo=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

class Advice(Base):
    __tablename__ = 'advice'
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)

Base.metadata.create_all(bind=engine)


import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class ContentGap(Base):
    __tablename__ = "content_gaps"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    demand_score = Column(Float)
    sources = Column(String)

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)

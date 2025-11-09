import os
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, create_engine, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
connect_args = {"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class MeasurementEntity(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String, index=True)
    parameter = Column(String)
    value = Column(Float)
    unit = Column(String)
    timestamp = Column(DateTime)


def init_db():
    Base.metadata.create_all(bind=engine)

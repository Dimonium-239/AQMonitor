import os
import uuid

from dotenv import load_dotenv
from sqlalchemy import Column, create_engine, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()
Base = declarative_base()

def get_engine():
    db_url = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    connect_args = {"check_same_thread": False} if "sqlite" in db_url else {}
    return create_engine(db_url, connect_args=connect_args)

engine = get_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class MeasurementEntity(Base):
    __tablename__ = "measurements"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    city = Column(String, index=True)
    parameter = Column(String)
    value = Column(Float)
    unit = Column(String)
    timestamp = Column(DateTime)

def init_db():
    Base.metadata.create_all(bind=engine)

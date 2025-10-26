import os
import uuid

from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
connect_args = {"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class MeasurementDB(Base):
    __tablename__ = "measurements"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))  # 🧠 auto-generate UUID
    city = Column(String, index=True)
    parameter = Column(String)
    value = Column(Float)
    unit = Column(String)
    timestamp = Column(DateTime)

    def __str__(self) -> str:
        """User-friendly string representation"""
        return f"Measurement(id={self.id}, city={self.city}, parameter={self.parameter}, value={self.value}, unit={self.unit}, timestamp={self.timestamp})"

    def __repr__(self) -> str:
        """Developer-friendly representation"""
        return f"<MeasurementDB id={self.id} city={self.city} parameter={self.parameter} value={self.value} unit={self.unit} timestamp={self.timestamp}>"

def init_db():
    Base.metadata.create_all(bind=engine)

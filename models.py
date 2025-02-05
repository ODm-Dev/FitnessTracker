from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

# Get database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create engine and session
engine = create_engine(DATABASE_URL) if DATABASE_URL else None
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    exercise = Column(String, index=True)
    target = Column(Integer)
    start_date = Column(Date)
    duration_days = Column(Integer)
    completed = Column(Boolean, default=False)

class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    exercise = Column(String, index=True)
    date = Column(Date)
    quantity = Column(Integer)

def init_db():
    """Initialize database tables"""
    if engine is not None:
        Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    if engine is None:
        raise Exception("Database URL not configured")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database tables
init_db()
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, Float, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime
import streamlit as st

# Get database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create engine with SSL and connection pooling settings
engine = None
if DATABASE_URL:
    try:
        engine = create_engine(
            DATABASE_URL,
            pool_size=5,
            max_overflow=2,
            pool_timeout=30,
            pool_recycle=1800,
            connect_args={
                "sslmode": "require"
            }
        )
    except Exception as e:
        st.error(f"Failed to create database engine: {str(e)}")

# Create session factory
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
        try:
            Base.metadata.create_all(bind=engine)
        except Exception as e:
            st.error(f"Failed to create database tables: {str(e)}")
            raise

def get_db():
    """Get database session"""
    if engine is None:
        raise Exception("Database URL not configured")

    db = SessionLocal()
    try:
        # Test the connection with proper text() wrapper
        db.execute(text("SELECT 1"))
        return db
    except Exception as e:
        db.close()
        raise Exception(f"Failed to connect to database: {str(e)}")

# Initialize database tables
init_db()
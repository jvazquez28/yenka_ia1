# src/database/__init__.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base
from config.settings import DATABASE_URL
import logging

logger = logging.getLogger(__name__)

def initialize_database():
    """Initialize PostgreSQL database with all tables"""
    try:
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(engine)
        logger.info("Database initialized successfully")
        return engine
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise
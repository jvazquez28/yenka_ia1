# src/database/__init__.py
from src.database.models import Base
from config.settings import DATABASE_URL
from sqlalchemy import create_engine
import logging

logger = logging.getLogger(__name__)

def initialize_database():
    """Initialize PostgreSQL database with all tables"""
    try:
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

if __name__ == "__main__":
    initialize_database()
# config/settings.py
from dotenv import load_dotenv
import os

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
YAHOO_FINANCE_API_KEY = os.getenv("YAHOO_FINANCE_API_KEY")

# PostgreSQL Database Configuration
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

DATABASE_URL = (
    f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)

# Other settings
DEBUG = os.getenv("DEBUG", "False") == "True"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
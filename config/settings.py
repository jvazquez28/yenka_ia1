# config/settings.py
from dotenv import load_dotenv
import os

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
YAHOO_FINANCE_API_KEY = os.getenv("YAHOO_FINANCE_API_KEY")

# Database
DATABASE_PATH = os.getenv("DATABASE_PATH", "financial_data.db")

# Other settings
DEBUG = os.getenv("DEBUG", "False") == "True"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
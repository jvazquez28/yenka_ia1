# src/agents/data_fetcher.py
from typing import Dict, Optional
import pandas as pd
import logging
from src.database.operations import DatabaseOperations
from src.api.alpha_vantage import fetch_alpha_vantage_data  # Ensure this is correctly implemented

logger = logging.getLogger(__name__)

class DataFetcher:
    def __init__(self, db_ops: DatabaseOperations):
        logger.info("Initializing DataFetcher")
        self.db_ops = db_ops

    def fetch_data(self, query_params: Dict[str, str]) -> Optional[pd.DataFrame]:
        """Fetches data based on query parameters, either from DB or API"""
        ticker = query_params.get("ticker")
        start_date = query_params.get("start_date")
        end_date = query_params.get("end_date")
        timeframe = query_params.get("timeframe")

        logger.info(f"Fetching data for ticker: {ticker}, timeframe: {timeframe}, dates: {start_date} to {end_date}")

        try:
            # Attempt to retrieve data from the database
            data = self.db_ops.get_stock_data(ticker, start_date, end_date, timeframe)
            if data is not None and not data.empty:
                logger.info("Data retrieved from database")
                return data
            
            # If data not found, fetch from external API
            logger.info("Data not found in database. Fetching from API")
            api_data = fetch_alpha_vantage_data(query_params)
            
            if api_data is not None and not api_data.empty:
                logger.info("Data fetched from API successfully")
                
                # Save fetched data to the database
                self.db_ops.save_stock_data(api_data)
                logger.info("Fetched data saved to database")
                
                return api_data
            else:
                logger.warning("No data returned from API")
                return None

        except Exception as e:
            logger.error(f"Error fetching data: {str(e)}")
            raise
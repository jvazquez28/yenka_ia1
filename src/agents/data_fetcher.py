# src/agents/data_fetcher.py
from typing import Dict, Optional
import pandas as pd
import logging
from datetime import datetime
from src.api.alpha_vantage import fetch_alpha_vantage_data
from src.database.operations import DatabaseOperations
from src.database.models import FundamentalData, OHLCData

logger = logging.getLogger(__name__)

class DataFetcher:
    def __init__(self, db_ops: DatabaseOperations):
        logger.info("Initializing DataFetcher")
        self.db_ops = db_ops

    def fetch_data(self, query_params: Dict[str, str]) -> Optional[pd.DataFrame]:
        logger.info(f"Fetching data with params: {query_params}")
        
        try:
            # Try to get data from database first
            data = self.db_ops.get_stock_data(
                ticker=query_params["ticker"],
                start_date=query_params["start_date"],
                end_date=query_params["end_date"],
                timeframe=query_params["timeframe"]
            )
            
            if data is not None and not data.empty:
                logger.info("Data found in database")
                return data
                
            # If no data in database, fetch from API
            logger.info("Fetching data from API")
            api_data = fetch_alpha_vantage_data(query_params)
            
            if not api_data.empty:
                logger.info("Successfully fetched data from API")
                
                # Prepare data for database
                fundamental_data = {
                    'ticker': query_params['ticker'],
                    'asset_name': api_data['ticker'].iloc[0],  # You might want to get proper name
                    'asset_type': 'stock'
                }
                
                # Save to database
                self.db_ops.save_stock_data(api_data)
                logger.info("Data saved to database")
                
                return api_data
            else:
                logger.warning("No data available from API")
                return None
                
        except Exception as e:
            logger.error(f"Error in fetch_data: {str(e)}")
            raise
# src/agents/data_fetcher.py
from typing import Dict
import pandas as pd
import logging
from src.api.alpha_vantage import fetch_alpha_vantage_data
from src.api.yahoo_finance import fetch_yahoo_finance_data
from src.database.operations import DatabaseOperations

logger = logging.getLogger(__name__)

class DataFetcher:
    """Clase para recuperar datos de activos de la base de datos o de una API externa"""

    def __init__(self, db_ops: DatabaseOperations):
        logger.info("Initializing DataFetcher")
        self.db_ops = db_ops

    def fetch_data(self, query_params: Dict[str, str]) -> pd.DataFrame:
        logger.info(f"Fetching data with params: {query_params}")
        
        try:
            logger.debug("Attempting to fetch data from database")
            data = self.db_ops.get_stock_data(
                ticker=query_params["ticker"],
                start_date=query_params["start_date"],
                end_date=query_params["end_date"],
                timeframe=query_params["timeframe"]
            )
            
            if data is not None and not data.empty:
                logger.info("Data found in database")
                return data
            else:
                logger.info("Data not found in database, fetching from external API")
                data = fetch_alpha_vantage_data(query_params)
                
                if not data.empty:
                    logger.info("Data fetched from API, saving to database")
                    self.db_ops.save_stock_data(data)
                else:
                    logger.warning("No data returned from API")
                    
                return data
                
        except Exception as e:
            logger.error(f"Error fetching data: {str(e)}")
            raise
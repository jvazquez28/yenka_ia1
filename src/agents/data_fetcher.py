# src/agents/data_fetcher.py
from src.api.alpha_vantage import fetch_alpha_vantage_data
from src.api.yahoo_finance import fetch_yahoo_finance_data
from src.database.operations import DatabaseOperations
import pandas as pd
from typing import Dict

class DataFetcher:
    def __init__(self, db_ops: DatabaseOperations):
        self.db_ops = db_ops

    def fetch_data(self, query_params: Dict[str, str]) -> pd.DataFrame:
        data = self.db_ops.get_stock_data(
            ticker=query_params["ticker"],
            start_date=query_params["start_date"],
            end_date=query_params["end_date"],
            timeframe=query_params["timeframe"]
        )
        if data is not None and not data.empty:
            return data
        else:
            # Fetch from external API
            data = fetch_alpha_vantage_data(query_params)  # or fetch_yahoo_finance_data
            if not data.empty:
                self.db_ops.save_stock_data(data)
            return data
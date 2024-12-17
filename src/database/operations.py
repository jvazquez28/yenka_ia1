# src/database/operations.py
import sqlite3
from typing import Optional, List
import pandas as pd
from src.database.models import create_tables

class DatabaseOperations:
    def __init__(self, db_path: str):
        self.db_path = db_path
        create_tables(self.db_path)

    def get_stock_data(self, ticker: str, start_date: str, end_date: str, timeframe: str) -> Optional[pd.DataFrame]:
        with sqlite3.connect(self.db_path) as conn:
            query = """
            SELECT * FROM financial_data
            WHERE ticker = ? AND timeframe = ? AND date BETWEEN ? AND ?
            ORDER BY date ASC
            """
            df = pd.read_sql_query(query, conn, params=(ticker, timeframe, start_date, end_date))
            return df if not df.empty else None

    def save_stock_data(self, data: pd.DataFrame):
        with sqlite3.connect(self.db_path) as conn:
            data.to_sql('financial_data', conn, if_exists='append', index=False)
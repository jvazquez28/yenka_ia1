# src/database/operations.py
from typing import Optional
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import FundamentalData, OHLCData, BacktestSummary, BacktestDetails
from config.settings import DATABASE_URL
import logging

logger = logging.getLogger(__name__)

class DatabaseOperations:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)
        logger.info("Database connection initialized")

    def get_stock_data(self, ticker: str, start_date: str, end_date: str, timeframe: str) -> Optional[pd.DataFrame]:
        """Retrieve OHLCV data from PostgreSQL database"""
        try:
            with self.Session() as session:
                query = """
                SELECT o.* 
                FROM ohlc_data o
                WHERE o.ticker = :ticker 
                AND o.timeframe = :timeframe 
                AND o.bar_date BETWEEN :start_date AND :end_date
                ORDER BY o.bar_date ASC, o.bar_time ASC
                """
                df = pd.read_sql_query(
                    query,
                    self.engine,
                    params={"ticker": ticker, "timeframe": timeframe, 
                           "start_date": start_date, "end_date": end_date}
                )
                return df if not df.empty else None
        except Exception as e:
            logger.error(f"Error retrieving stock data: {str(e)}")
            raise

    def save_stock_data(self, data: pd.DataFrame):
        """Save OHLCV data to PostgreSQL database"""
        try:
            with self.Session() as session:
                # First, ensure fundamental data exists
                fundamental = FundamentalData(
                    ticker=data['ticker'].iloc[0],
                    asset_name=data.get('asset_name', data['ticker'].iloc[0]),
                    asset_type='stock'  # Default value, can be updated later
                )
                session.merge(fundamental)
                
                # Then save OHLCV data
                ohlc_records = []
                for _, row in data.iterrows():
                    ohlc = OHLCData(
                        ticker=row['ticker'],
                        bar_date=row['date'],
                        bar_time=row.get('time', '00:00:00'),
                        timeframe=row['timeframe'],
                        open_price=row['open'],
                        high_price=row['high'],
                        low_price=row['low'],
                        close_price=row['close'],
                        volume=row['volume']
                    )
                    ohlc_records.append(ohlc)
                
                session.bulk_save_objects(ohlc_records)
                session.commit()
                logger.info(f"Saved {len(ohlc_records)} records for {data['ticker'].iloc[0]}")
        except Exception as e:
            logger.error(f"Error saving stock data: {str(e)}")
            raise

    def save_backtest_summary(self, backtest_data: dict):
        """Save backtest summary results"""
        try:
            with self.Session() as session:
                summary = BacktestSummary(**backtest_data)
                session.add(summary)
                session.commit()
                logger.info(f"Saved backtest summary for {backtest_data['ticker']}")
                return summary.test_id
        except Exception as e:
            logger.error(f"Error saving backtest summary: {str(e)}")
            raise

    def save_backtest_details(self, test_id: int, trades_data: list):
        """Save backtest trade details"""
        try:
            with self.Session() as session:
                trade_records = []
                for trade in trades_data:
                    trade['test_id'] = test_id
                    trade_record = BacktestDetails(**trade)
                    trade_records.append(trade_record)
                
                session.bulk_save_objects(trade_records)
                session.commit()
                logger.info(f"Saved {len(trade_records)} trade records for test_id {test_id}")
        except Exception as e:
            logger.error(f"Error saving backtest details: {str(e)}")
            raise
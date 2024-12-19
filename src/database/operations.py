# src/database/operations.py
from typing import Optional, Dict, List
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.database.models import FundamentalData, OHLCData, BacktestSummary, BacktestDetails
from config.settings import DATABASE_URL
import logging

logger = logging.getLogger(__name__)

class DatabaseOperations:
    def __init__(self):
        try:
            # Create PostgreSQL engine with psycopg2 driver
            self.engine = create_engine(DATABASE_URL, client_encoding='utf8')
            self.Session = sessionmaker(bind=self.engine)
            logger.info("PostgreSQL database connection initialized")
        except Exception as e:
            logger.error(f"Failed to initialize database connection: {str(e)}")
            raise

    def get_stock_data(self, ticker: str, start_date: str, end_date: str, timeframe: str) -> Optional[pd.DataFrame]:
        """Retrieve OHLCV data from PostgreSQL database"""
        try:
            with self.Session() as session:
                query = text("""
                    SELECT 
                        ticker,
                        bar_date,
                        bar_time,
                        timeframe,
                        open_price,
                        high_price,
                        low_price,
                        close_price,
                        volume
                    FROM ohlc_data
                    WHERE ticker = :ticker 
                    AND timeframe = :timeframe 
                    AND bar_date BETWEEN :start_date AND :end_date
                    ORDER BY bar_date ASC, bar_time ASC
                """)
                
                # Use pd.read_sql_query with SQLAlchemy engine
                df = pd.read_sql_query(
                    query,
                    self.engine,
                    params={
                        "ticker": ticker,
                        "timeframe": timeframe, 
                        "start_date": start_date, 
                        "end_date": end_date
                    }
                )
                return df if not df.empty else None
        except Exception as e:
            logger.error(f"Error retrieving stock data: {str(e)}")
            raise

    def save_stock_data(self, data: pd.DataFrame):
        """Save OHLCV data to PostgreSQL database"""
        try:
            with self.Session() as session:
                # Ensure correct column names
                data = data.rename(columns={
                    'date': 'bar_date',
                    'time': 'bar_time'
                })

                # Check if FundamentalData exists, if not, create it
                fundamental_ticker = data['ticker'].iloc[0]
                fundamental = session.query(FundamentalData).filter_by(ticker=fundamental_ticker).first()
                if not fundamental:
                    fundamental = FundamentalData(
                        ticker=fundamental_ticker,
                        asset_name=fundamental_ticker,  # Modify as needed
                        asset_type='stock'  # Modify as needed
                    )
                    session.add(fundamental)
                    session.commit()
                    logger.info(f"Added new fundamental data for ticker: {fundamental_ticker}")

                # Prepare OHLCData objects
                ohlc_records = [
                    OHLCData(
                        ticker=row['ticker'],
                        bar_date=row['bar_date'],
                        bar_time=row['bar_time'],
                        timeframe=row['timeframe'],
                        open_price=row['open_price'],
                        high_price=row['high_price'],
                        low_price=row['low_price'],
                        close_price=row['close_price'],
                        volume=row['volume']
                    ) for _, row in data.iterrows()
                ]

                # Bulk save
                session.bulk_save_objects(ohlc_records)
                session.commit()
                logger.info(f"Saved {len(ohlc_records)} OHLC records for ticker: {fundamental_ticker}")
        except Exception as e:
            logger.error(f"Error saving stock data: {str(e)}")
            raise

    def save_backtest_summary(self, backtest_data: dict) -> int:
        """Save backtest summary results and return the test_id"""
        try:
            with self.Session() as session:
                summary = BacktestSummary(**backtest_data)
                session.add(summary)
                session.commit()
                logger.info(f"Saved backtest summary for ticker: {backtest_data['ticker']}")
                return summary.test_id
        except Exception as e:
            logger.error(f"Error saving backtest summary: {str(e)}")
            raise

    def save_backtest_details(self, test_id: int, trades_data: List[dict]):
        """Save backtest trade details"""
        try:
            with self.Session() as session:
                trade_records = [
                    BacktestDetails(
                        test_id=test_id,
                        trade_number=trade['trade_number'],
                        buy_date=trade['buy_date'],
                        buy_time=trade['buy_time'],
                        sell_date=trade['sell_date'],
                        sell_time=trade['sell_time'],
                        buy_price=trade['buy_price'],
                        sell_price=trade['sell_price'],
                        position_size=trade['position_size'],
                        equity_after_trade=trade['equity_after_trade']
                    ) for trade in trades_data
                ]
                session.bulk_save_objects(trade_records)
                session.commit()
                logger.info(f"Saved {len(trade_records)} backtest detail records for test_id {test_id}")
        except Exception as e:
            logger.error(f"Error saving backtest details: {str(e)}")
            raise
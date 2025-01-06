# src/database/models.py
from sqlalchemy import (
    Column, Integer, BigInteger, String, Date, Time, Numeric,
    ForeignKey, CheckConstraint, UniqueConstraint, Text, DateTime, Interval,
    func
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from config.settings import DATABASE_URL

Base = declarative_base()

class FundamentalData(Base):
    __tablename__ = 'fundamental_data'

    ticker = Column(String(10), primary_key=True)
    asset_name = Column(String(100), nullable=False)
    industry = Column(String(100))
    asset_type = Column(String(20), CheckConstraint(
        "asset_type IN ('stock', 'etf', 'index', 'crypto', 'other')"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    ohlc_data = relationship('OHLCData', back_populates='fundamental_data', cascade='all, delete-orphan')
    backtest_summaries = relationship('BacktestSummary', back_populates='fundamental_data', cascade='all, delete-orphan')

class OHLCData(Base):
    __tablename__ = 'ohlc_data'

    ohlc_id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), ForeignKey('fundamental_data.ticker', ondelete='CASCADE'), nullable=False)
    bar_date = Column(Date, nullable=False)
    bar_time = Column(Time, nullable=False)
    timeframe = Column(String(10), nullable=False)  # e.g., '1min', '30min', 'daily'
    open_price = Column(Numeric(15, 6), nullable=False)
    high_price = Column(Numeric(15, 6), nullable=False)
    low_price = Column(Numeric(15, 6), nullable=False)
    close_price = Column(Numeric(15, 6), nullable=False)
    volume = Column(BigInteger, CheckConstraint('volume >= 0'))

    # Relationships
    fundamental_data = relationship('FundamentalData', back_populates='ohlc_data')

    # Constraints
    __table_args__ = (
        UniqueConstraint('ticker', 'bar_date', 'bar_time', 'timeframe', name='uix_ohlc_data'),
    )

class BacktestSummary(Base):
    __tablename__ = 'backtest_summary'

    test_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text, nullable=False)
    ticker = Column(String(10), ForeignKey('fundamental_data.ticker', ondelete='CASCADE'), nullable=False)
    strategy_name = Column(String(100), nullable=False)
    strategy_parameters = Column(Text)  # e.g., "SmaCross(n1=10, n2=20)"
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    duration = Column(Interval)
    exposure_time_pct = Column(Numeric(6, 2))
    equity_final = Column(Numeric(15, 2))
    equity_peak = Column(Numeric(15, 2))
    return_pct = Column(Numeric(10, 2))
    buy_hold_return_pct = Column(Numeric(10, 2))
    annual_return_pct = Column(Numeric(10, 2))
    annual_volatility_pct = Column(Numeric(10, 2))
    sharpe_ratio = Column(Numeric(6, 2))
    sortino_ratio = Column(Numeric(6, 2))
    calmar_ratio = Column(Numeric(6, 2))
    max_drawdown_pct = Column(Numeric(6, 2))
    avg_drawdown_pct = Column(Numeric(6, 2))
    max_drawdown_duration = Column(Interval)
    avg_drawdown_duration = Column(Interval)
    total_trades = Column(Integer, CheckConstraint('total_trades >= 0'))
    win_rate_pct = Column(Numeric(6, 2))
    best_trade_pct = Column(Numeric(6, 2))
    worst_trade_pct = Column(Numeric(6, 2))
    avg_trade_pct = Column(Numeric(6, 2))
    max_trade_duration = Column(Interval)
    avg_trade_duration = Column(Interval)
    profit_factor = Column(Numeric(6, 2))
    expectancy_pct = Column(Numeric(6, 2))
    sqn = Column(Numeric(6, 2))
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    fundamental_data = relationship('FundamentalData', back_populates='backtest_summaries')
    backtest_details = relationship('BacktestDetails', back_populates='backtest_summary', cascade='all, delete-orphan')

class BacktestDetails(Base):
    __tablename__ = 'backtest_details'

    detail_id = Column(Integer, primary_key=True, autoincrement=True)
    test_id = Column(Integer, ForeignKey('backtest_summary.test_id', ondelete='CASCADE'), nullable=False)
    trade_number = Column(Integer, CheckConstraint('trade_number > 0'), nullable=False)
    buy_date = Column(Date, nullable=False)
    buy_time = Column(Time, nullable=False)
    sell_date = Column(Date, nullable=False)
    sell_time = Column(Time, nullable=False)
    buy_price = Column(Numeric(15, 6), nullable=False)
    sell_price = Column(Numeric(15, 6), nullable=False)
    position_size = Column(Integer, CheckConstraint('position_size > 0'))
    trade_duration = Column(Interval, server_default='0 seconds')  # Generated always
    trade_return_pct = Column(Numeric(10, 2), server_default='0')
    profit_loss = Column(Numeric(15, 2), server_default='0')
    equity_after_trade = Column(Numeric(15, 2))

    # Relationships
    backtest_summary = relationship('BacktestSummary', back_populates='backtest_details')

    # Constraints
    __table_args__ = (
        UniqueConstraint('test_id', 'trade_number', name='uix_backtest_details'),
    )
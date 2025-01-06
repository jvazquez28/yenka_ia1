#two_sma.py
import logging
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import pandas as pd
from src.database.operations import DatabaseOperations
import numpy as np

logger = logging.getLogger(__name__)

class TwoSMA(Strategy):
    n_slow = 20
    n_fast = 10

    def init(self):
        logger.info(f"Initializing TwoSMA strategy with slow={self.n_slow}, fast={self.n_fast}")
        try:
            # Convert Close prices to numpy array and calculate SMAs directly
            close = np.array(self.data.Close)
            
            # Calculate moving averages using numpy
            #self.ma_slow = self.I(lambda x: pd.Series(x).rolling(self.n_slow).mean(), close)
            #self.ma_fast = self.I(lambda x: pd.Series(x).rolling(self.n_fast).mean(), close)
            self.ma_slow = self.I(SMA, close, self.n_slow)
            self.ma_fast = self.I(SMA, close, self.n_fast)

            logger.info("Successfully initialized moving averages")
        except Exception as e:
            logger.error(f"Failed during rolling calculations: {str(e)}")
            raise

    def next(self):
        if crossover(self.ma_fast, self.ma_slow):
            self.buy()
        elif crossover(self.ma_slow, self.ma_fast):
            self.sell()

def run_two_sma_backtest(data: pd.DataFrame, db_ops: DatabaseOperations, ticker: str):
    logger.info("Starting two SMA backtest")
    try:
        # Prepare data for backtesting.py
        bt_data = data.rename(columns={
            'close_price': 'Close',
            'high_price': 'High',
            'low_price': 'Low',
            'open_price': 'Open',
            'volume': 'Volume'
        })
        bt_data.index = pd.date_range(
            start=bt_data['bar_date'].iloc[0],
            periods=len(bt_data),
            freq='D'
        )
        bt_data.drop(['bar_date', 'bar_time', 'timeframe', 'ticker'], axis=1, inplace=True)

        logger.info(f"Data prepared for backtesting. Rows: {len(bt_data)}")
        
        bt = Backtest(bt_data, TwoSMA, cash=10000, commission=0.001)
        result = bt.run()
        
        logger.info(f"Backtest completed. Available stats: {result.keys()}")
        
        # Calculate buy & hold return
        #first_close = bt_data['Close'].iloc[0]
        #last_close = bt_data['Close'].iloc[-1]
        #buy_hold_return_pct = (last_close - first_close) / first_close * 100

        # Save backtest summary with corrected keys
        summary_data = {
            'description': 'TwoSMA vs BuyHold',
            'ticker': ticker,
            'strategy_name': 'TwoSMA(10,20)',
            'strategy_parameters': 'Fast=10,Slow=20',
            'start_date': result['Start'],
            'end_date': result['End'],
            'duration': result['Duration'],
            #'start_date': data['bar_date'].iloc[0],
            #'end_date': data['bar_date'].iloc[-1],
            #'duration': str(result['Duration']),
            'exposure_time_pct': float(result['Exposure Time [%]']),
            'equity_final': float(result['Equity Final [$]']),
            'equity_peak': float(result['Equity Peak [$]']),
            'return_pct': float(result['Return [%]']),
            'buy_hold_return_pct': float(result['Buy & Hold Return [%]']),
            'annual_return_pct': float(result['Return (Ann.) [%]']),
            'annual_volatility_pct': float(result['Volatility (Ann.) [%]']),
            'sharpe_ratio': float(result['Sharpe Ratio']),
            'sortino_ratio': float(result['Sortino Ratio']),
            'calmar_ratio': float(result['Calmar Ratio']),
            'max_drawdown_pct': float(result['Max. Drawdown [%]']),
            'avg_drawdown_pct': float(result['Avg. Drawdown [%]']),
            'max_drawdown_duration': str(result['Max. Drawdown Duration']),
            'avg_drawdown_duration': str(result['Avg. Drawdown Duration']),
            'total_trades': int(result['# Trades']),
            'win_rate_pct': float(result['Win Rate [%]']),
            'best_trade_pct': float(result['Best Trade [%]']),
            'worst_trade_pct': float(result['Worst Trade [%]']),
            'avg_trade_pct': float(result['Avg. Trade [%]']),
            'max_trade_duration': str(result['Max. Trade Duration']),
            'avg_trade_duration': str(result['Avg. Trade Duration']),
            'profit_factor': float(result['Profit Factor']),
            'expectancy_pct': float(result['Expectancy [%]']),
            'sqn': float(result['SQN'])
        }
        test_id = db_ops.save_backtest_summary(summary_data)
        logger.info(f"Backtest summary saved with test_id={test_id}")

        # Save backtest details
        detail_records = []
        for i, trade in result['_trades'].iterrows():
            detail_records.append({
                'trade_number': i + 1,
                'buy_date': trade['EntryTime'].date(),
                'buy_time': trade['EntryTime'].time(),
                'sell_date': trade['ExitTime'].date(),
                'sell_time': trade['ExitTime'].time(),
                'buy_price': float(trade['EntryPrice']),
                'sell_price': float(trade['ExitPrice']),
                'position_size': int(np.round(trade['Size'])),
                'equity_after_trade': None
            })
        db_ops.save_backtest_details(test_id, detail_records)
        logger.info(f"Backtest details saved for {len(detail_records)} trades")

        return result #, buy_hold_return_pct
    
    except Exception as e:
        logger.error(f"Error during two_SMA_backtest: {str(e)}")
        raise
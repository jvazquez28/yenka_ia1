# src/database/models.py
import sqlite3

def create_tables(db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS financial_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        date DATE NOT NULL,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume INTEGER,
        timeframe TEXT NOT NULL
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fundamental_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        metric_name TEXT NOT NULL,
        value REAL,
        date DATE NOT NULL,
        FOREIGN KEY (ticker) REFERENCES financial_data (ticker)
    );
    """)
    
    conn.commit()
    conn.close()
# frontend/app.py
import logging
import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd
import requests
import sys
from pathlib import Path
import plotly.express as px
from typing import Optional
import matplotlib.pyplot as plt



# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_assistant.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))
logger.info(f"Added {ROOT_DIR} to Python path")


from config.settings import OPENAI_API_KEY, DATABASE_URL
from src.database.operations import DatabaseOperations
from src.agents.query_parser import QueryParser
from src.agents.data_fetcher import DataFetcher
from frontend.styles.trading_theme import load_trading_theme


def initialize_llm() -> Optional[QueryParser]:
    try:
        if not OPENAI_API_KEY:
            logger.error("OpenAI API key not found")
            st.error("OpenAI API key not found")
            return None
        
        logger.info("Initializing QueryParser with OpenAI API")
        parser = QueryParser()
        logger.info("QueryParser initialized successfully")
        return parser
    except Exception as e:
        logger.error(f"Failed to initialize QueryParser: {str(e)}")
        st.error(f"Failed to initialize QueryParser: {str(e)}")
        return None

def main():
    # Load environment variables and theme
    load_dotenv()
    st.markdown(load_trading_theme(), unsafe_allow_html=True)

    # Initialize QueryParser
    parser = initialize_llm()
    if parser is None:
        st.stop()

    # Initialize database operations
    try:
        db_ops = DatabaseOperations()
        logger.info("Database operations initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        st.error("Failed to connect to database")
        st.stop()

    # Initialize DataFetcher
    fetcher = DataFetcher(db_ops)

    # Layout and input
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        st.title("📈 Yenka IA1 Trading Assistant")
    
    with st.container():
        st.markdown("### 💬 Query Input")
        query = st.text_input(
            "Ingrese su consulta financiera en lenguaje natural:", 
            "Mostrar datos diarios de AAPL del último año"
        )
    
    if st.button("Analizar"):
        if not query.strip():
            st.warning("Por favor, ingrese una consulta válida.")
            st.stop()

        try:
            # Parse query
            parsed_query = parser.parse_query(query)
            logger.info(f"Parsed query: {parsed_query}")
            
            # Fetch data
            data = fetcher.fetch_data(parsed_query)
            
            if data is not None and not data.empty:
                st.success("Datos obtenidos exitosamente")
                
                # Display data
                with st.expander("Ver datos"):
                    st.dataframe(data)
                
                # Calculate SMAs
                data['SMA_10'] = data['close_price'].rolling(window=10).mean()
                data['SMA_20'] = data['close_price'].rolling(window=20).mean()
                
                # Create price chart with SMAs
                fig = px.line(
                    data,
                    x='bar_date',
                    y=['close_price', 'SMA_10', 'SMA_20'],
                    labels={
                        'bar_date': 'Fecha',
                        'value': 'Precio',
                        'variable': 'Indicador',
                        'close_price': 'Precio',
                        'SMA_10': 'Media Móvil 10',
                        'SMA_20': 'Media Móvil 20'
                    },
                    title=f'Precios de {parsed_query["ticker"].upper()}'
                )
                st.plotly_chart(fig)

                # Run backtest
                from src.backtesting.two_sma import run_two_sma_backtest
                logger.info("Executing the Two-SMA backtest")
                ticker = parsed_query["ticker"]
                try:
                    #result, buy_hold_return_pct = run_two_sma_backtest(data, db_ops, ticker)
                    result = run_two_sma_backtest(data, db_ops, ticker)
                    st.success("Backtest completado correctamente. Resultados almacenados en la base de datos.")

                    # Display backtest results
                    st.write("### Resultados del Backtest")
                    st.write(result)

                    # Display backtest plots
                    #st.write("### Gráficos del Backtest")
                    #try:
                        # Use a default style that's guaranteed to exist    
                        #plt.style.use('default')

                        # Create figure with larger size
                        #plt.figure(figsize=(12, 8))

                        #fig_backtest = result.plot()
                        #st.pyplot(fig_backtest, clear_figure=True)

                    #except Exception as e:
                        #logger.error(f"Error generating backtest plot: {str(e)}")
                        #st.error("No se pudo generar el gráfico del backtest")

                except Exception as e:
                    logger.error(f"Error processing backtest: {str(e)}")
                    st.error(f"Hubo un error ejecutando el backtest: {str(e)}")

            else:
                st.warning("No se encontraron datos para esta consulta.")
                
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            st.error(f"Error al procesar la consulta: {str(e)}")

if __name__ == "__main__":
    main()
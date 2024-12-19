# frontend/app.py
import logging
import streamlit as st
from langchain_community.llms.openai import OpenAI
from langchain_community.tools import Tool
from dotenv import load_dotenv
import os
import pandas as pd
import requests
import sys
from pathlib import Path


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


# Import custom modules
from src.agents.query_parser import QueryParser
from src.agents.data_fetcher import DataFetcher
from src.database.operations import DatabaseOperations
from config.settings import OPENAI_API_KEY #, DATABASE_PATH
from frontend.styles.trading_theme import load_trading_theme


#Inicialización de instancia OpenAI
def initialize_llm():
    logger.info("Initializing OpenAI LLM...")
    try:
        if not OPENAI_API_KEY:
            logger.error("OpenAI API key not found")
            raise ValueError("OpenAI API key not found")
        
        llm = OpenAI(
            api_key=OPENAI_API_KEY,
            temperature=0.5,
            model_name="gpt-3.5-turbo-instruct" # selección de modelo
        )
        logger.info("OpenAI LLM initialized successfully")
        return llm
    
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {str(e)}")
        st.error(f"Failed to initialize LLM: {str(e)}")
        return None

def main():
    # Load environment variables and theme
    load_dotenv()
    st.markdown(load_trading_theme(), unsafe_allow_html=True)
    
    # Initialize OpenAI and database
    llm = initialize_llm()
    if llm is None:
        st.stop()

    # Initialize database operations
    try:
        db_ops = DatabaseOperations()  # Remove DATABASE_PATH as it's not needed for PostgreSQL
        logger.info("Database operations initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        st.error("Failed to connect to database")
        st.stop()

    # Layout and input
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        st.title("📈 Yenka IA1 Trading Assistant")
    
    with st.container():
        st.markdown("### 💬 Query Input")
        query = st.text_input(
            "Ingrese su consulta financiera en lenguaje natural:", 
            "Mostrar datos diarios de AAPL del último mes"
        )
    
    if st.button("Analizar"):
        try:
            # Parse query
            parser = QueryParser(llm)
            parsed_query = parser.parse_query(query)
            logger.info(f"Parsed query: {parsed_query}")
            
            # Fetch data
            fetcher = DataFetcher(db_ops)
            data = fetcher.fetch_data(parsed_query)
            
            if data is not None and not data.empty:
                st.success("Datos obtenidos exitosamente")
                
                # Display data
                with st.expander("Ver datos"):
                    st.dataframe(data)
                
                # Create price chart
                fig = px.line(
                    data,
                    x='bar_date',
                    y=['open_price', 'close_price', 'high_price', 'low_price'],
                    title=f'Precios de {parsed_query["ticker"]}'
                )
                st.plotly_chart(fig)
            else:
                st.warning("No se encontraron datos para esta consulta")
                
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            st.error(f"Error al procesar la consulta: {str(e)}")

    # Configuración de LangChain con herramientas
    query_tool = Tool(
        name="QueryDatabase",
        func=lambda inputs: db_ops.get_stock_data(**inputs),
        description="Consulta los datos financieros en la base de datos."
    )
    
    fetch_tool = Tool(
        name="FetchData",
        func=lambda inputs: fetcher.fetch_data(inputs),
        description="Obtiene datos financieros desde la API externa si no están en la base de datos."
    )

if __name__ == "__main__":
    main()
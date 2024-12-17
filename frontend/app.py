# frontend/app.py
import streamlit as st
from langchain.llms import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
import requests
from src.agents.query_parser import QueryParser
from src.agents.data_fetcher import DataFetcher
from src.database.operations import DatabaseOperations
from config.settings import OPENAI_API_KEY, DATABASE_PATH

def main():
    load_dotenv()
    
    st.title("Yenka IA1 Trading Assistant")
    
    query = st.text_input("Ingrese su consulta financiera en lenguaje natural:", 
                          "Mostrar datos diarios de AAPL del último mes")
    
    if st.button("Analizar"):
        llm = OpenAI(api_key=OPENAI_API_KEY)
        parser = QueryParser(llm)
        parsed_query = parser.parse_query(query)
        
        db_ops = DatabaseOperations(DATABASE_PATH)
        fetcher = DataFetcher(db_ops)
        data = fetcher.fetch_data(parsed_query)
        
        if not data.empty:
            st.success("Datos obtenidos de la base de datos.")
            st.dataframe(data)
            # Aquí puedes agregar análisis técnico
            st.line_chart(data.set_index('date')['close'])
        else:
            st.error("No se encontraron datos. Intentando obtener desde la API externa...")
            # Implementar la lógica para fetch_data_from_api_tool
            api_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={parsed_query['ticker']}&apikey={os.getenv('ALPHA_VANTAGE_API_KEY')}"
            response = requests.get(api_url)
    
            if response.status_code == 200:
                data = response.json()
                # Convertir datos al formato esperado
                formatted_data = [
                    (parsed_query["ticker"], item["date"], item["open"], item["high"], item["low"], item["close"], item["volume"], parsed_query["timeframe"])
                    for item in data.get("Time Series (Daily)", [])
                ]
    
                # Guardar datos en la base de datos
                conn = db_ops.connect_db()
                conn.executemany(
                    """
                    INSERT INTO financial_data (ticker, date, open, high, low, close, volume, timeframe)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, formatted_data
                )
                conn.commit()
                conn.close()
    
                st.success("Datos obtenidos de la API externa y almacenados en la base de datos.")
                df = pd.DataFrame(formatted_data, columns=["ticker", "date", "open", "high", "low", "close", "volume", "timeframe"])
                st.dataframe(df)
                st.line_chart(df.set_index('date')['close'])
            else:
                st.error("Error al conectar con la API")

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
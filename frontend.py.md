import streamlit as st
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.tools import BaseTool
from langchain.memory import ConversationBufferMemory
import sqlite3
import requests
import pandas as pd
from dotenv import load_dotenv
import os
import plotly.express as px

# Configuración de la API de OpenAI
# Cargar variables de entorno desde el archivo .env
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(model="text-davinci-003", openai_api_key=openai_api_key)

# Configuración de la base de datos
DATABASE = "financial_data.db"

def connect_db():
    return sqlite3.connect(DATABASE)

# Herramienta para consultar la base de datos
def query_database_tool(inputs):
    conn = connect_db()
    ticker = inputs["ticker"]
    start_date = inputs["start_date"]
    end_date = inputs["end_date"]
    timeframe = inputs["timeframe"]

    query = """
    SELECT * FROM financial_data
    WHERE ticker = ? AND timeframe = ? AND date BETWEEN ? AND ?
    """
    result = conn.execute(query, (ticker, timeframe, start_date, end_date)).fetchall()
    conn.close()

    if result:
        return {
            "status": "success",
            "data": pd.DataFrame(result, columns=["id", "ticker", "date", "open", "high", "low", "close", "volume", "timeframe"])
        }
    else:
        return {"status": "not_found"}

# Herramienta para extraer datos de la API
def fetch_data_from_api_tool(inputs):
    ticker = inputs["ticker"]
    timeframe = inputs["timeframe"]

    # Ejemplo de API (Placeholder, reemplazar con API real)
    api_url = f"https://api.example.com/data?ticker={ticker}&timeframe={timeframe}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        # Convertir datos al formato esperado
        formatted_data = [
            (ticker, item["date"], item["open"], item["high"], item["low"], item["close"], item["volume"], timeframe)
            for item in data
        ]

        # Guardar datos en la base de datos
        conn = connect_db()
        conn.executemany(
            """
            INSERT INTO financial_data (ticker, date, open, high, low, close, volume, timeframe)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, formatted_data
        )
        conn.commit()
        conn.close()

        return {"status": "success", "data": pd.DataFrame(formatted_data, columns=["ticker", "date", "open", "high", "low", "close", "volume", "timeframe"])}
    else:
        return {"status": "error", "message": "Error al conectar con la API"}

# Configuración de LangChain con herramientas
query_tool = Tool(
    name="QueryDatabase",
    func=query_database_tool,
    description="Consulta los datos financieros en la base de datos."
)

fetch_tool = Tool(
    name="FetchData",
    func=fetch_data_from_api_tool,
    description="Obtiene datos financieros de una API externa."
)

memory = ConversationBufferMemory()
agent = initialize_agent([query_tool, fetch_tool], llm, memory=memory, agent="conversational")

# Interfaz con Streamlit
st.title("AI Trading Assistant - Plataforma de Trading")

# Entrada del usuario
prompt = st.text_input("Escribe tu consulta en lenguaje natural:", "Dame los datos históricos de Tesla para el último año con gráficos diarios.")

if prompt:
    with st.spinner("Procesando tu solicitud..."):
        # El agente procesa el prompt
        response = agent.run(prompt)

        # Mostrar resultados
        if response.get("status") == "success":
            st.success("Datos encontrados o extraídos exitosamente.")
            data = response["data"]
            # Mostrar tabla de datos
            st.dataframe(data)

            # Graficar datos
            fig = px.line(data, x="date", y="close", title=f"Precio de cierre de {response['data']['ticker'][0]}")
            st.plotly_chart(fig)
        elif response.get("status") == "not_found":
            st.warning("No se encontraron datos y no se pudieron extraer de la API.")
        else:
            st.error("Hubo un problema al procesar tu solicitud.")

# frontend/components/query_input.py
import streamlit as st

def get_user_query() -> str:
    query = st.text_input("Ingrese su consulta financiera:", 
                          "Mostrar datos diarios de AAPL del último mes")
    return query
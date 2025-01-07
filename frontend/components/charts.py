# frontend/components/charts.py
import streamlit as st
import pandas as pd
import plotly.express as px

def display_chart(data: pd.DataFrame, column: str = "close"):
    fig = px.line(data, x='date', y=column, title=f'{column.capitalize()} Over Time')
    st.plotly_chart(fig)
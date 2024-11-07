# secciones/mapa_calor.py
import streamlit as st
import pandas as pd
import folium
import numpy as np
import plotly.express as px
from folium.plugins import HeatMap
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

def generar_mapa_calor(df3, centro_df):
    st.subheader("Mapa de Calor de Centros de Vacunación")
    
    # Mapa de Calor
    mapa = folium.Map(location=[centro_df['latitud'].values[0], centro_df['longitud'].values[0]], zoom_start=15)
    heat_data = [[row['latitud'], row['longitud']] for index, row in df3.iterrows()]
    HeatMap(heat_data).add_to(mapa)
    st_folium(mapa, width=700, height=500)


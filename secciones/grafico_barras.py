# secciones/grafico_barras.py
import streamlit as st
import pandas as pd
import folium
import numpy as np
import plotly.express as px
from folium.plugins import HeatMap
import plotly.express as px
import streamlit as st

def generar_grafico_barras(df3, region_seleccionada, provincia_seleccionada, distrito_seleccionado):
    st.subheader("Gráfico de Barras de Centros de Vacunación")
    
    # Gráfico de barras: Número de Centros por Región/Provincia/Distrito
    if region_seleccionada != "Seleccione una opción":
        if provincia_seleccionada == "Seleccione una opción":
            datos_agrupados = df3[df3['region'] == region_seleccionada].groupby('provincia').size().reset_index(name='centros')
            titulo = f"Centros de Vacunación en la Región {region_seleccionada} por Provincia"
        elif distrito_seleccionado == "Seleccione una opción":
            datos_agrupados = df3[(df3['region'] == region_seleccionada) & (df3['provincia'] == provincia_seleccionada)].groupby('distrito').size().reset_index(name='centros')
            titulo = f"Centros de Vacunación en la Provincia {provincia_seleccionada} por Distrito"
        else:
            datos_agrupados = df3[(df3['region'] == region_seleccionada) & (df3['provincia'] == provincia_seleccionada) & (df3['distrito'] == distrito_seleccionado)].groupby('Centro_vacunacion').size().reset_index(name='centros')
            titulo = f"Centros de Vacunación en {distrito_seleccionado}"

        # Crear gráfico de barras con Plotly
        fig = px.bar(datos_agrupados, x=datos_agrupados.columns[0], y='centros', title=titulo)
        st.plotly_chart(fig)


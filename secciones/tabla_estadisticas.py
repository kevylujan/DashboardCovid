# secciones/tabla_estadisticas.py
import streamlit as st
import pandas as pd
import folium
import numpy as np
import plotly.express as px
from folium.plugins import HeatMap
import streamlit as st

def generar_tabla_estadisticas(df3, region_seleccionada, provincia_seleccionada, distrito_seleccionado):
    st.subheader("Tabla de Centros de Vacunación")
    tabla_filtrada = df3[(df3['region'] == region_seleccionada) & (df3['provincia'] == provincia_seleccionada) & (df3['distrito'] == distrito_seleccionado)]
    st.dataframe(tabla_filtrada)

    # Estadísticas resumidas
    st.subheader("Estadísticas Resumidas")
    estadisticas = {
        "Total de Centros en Región": df3[df3['region'] == region_seleccionada].shape[0],
        "Total de Centros en Provincia": df3[(df3['region'] == region_seleccionada) & (df3['provincia'] == provincia_seleccionada)].shape[0],
        "Total de Centros en Distrito": df3[(df3['region'] == region_seleccionada) & (df3['provincia'] == provincia_seleccionada) & (df3['distrito'] == distrito_seleccionado)].shape[0]
    }
    for key, value in estadisticas.items():
        st.metric(label=key, value=value

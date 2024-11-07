# dashboard.py
import streamlit as st
import pandas as pd
import folium
import numpy as np
import plotly.express as px
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from secciones.mapa_calor import generar_mapa_calor
from secciones.grafico_barras import generar_grafico_barras
from secciones.tabla_estadisticas import generar_tabla_estadisticas

# Carga de datos
@st.cache_data(show_spinner=False)
def cargar_datos():
    df = pd.read_csv("TB_CENTRO_VACUNACION.csv", sep=";")
    df1 = df.copy()
    df1.rename(columns={'nombre': 'Centro_vacunacion'}, inplace=True)
    df1.drop(['id_centro_vacunacion', 'id_eess'], axis=1, inplace=True)
    df1.replace('', np.nan, inplace=True)
    df1['entidad_administra'] = df1['entidad_administra'].fillna('No especificado')

    df_ubigeo = pd.read_csv("TB_UBIGEOS.csv", sep=";")
    df_ub = df_ubigeo[['id_ubigeo', 'provincia', 'distrito', 'region']]
    df3 = pd.merge(df1, df_ub, on='id_ubigeo', how='left')
    return df3

df3 = cargar_datos()

# Configuración de título y barra lateral
st.title("Dashboard de Centros de Vacunación")
st.sidebar.title("Elige los filtros")

# Agregar una opción "Seleccione una opción" al selectbox de región
region_opciones = ["Seleccione una opción"] + sorted(df3['region'].unique().tolist())
region_seleccionada = st.sidebar.selectbox("Seleccione la región", options=region_opciones)

# Variables para almacenar los valores seleccionados
provincia_seleccionada = "Seleccione una opción"
distrito_seleccionado = "Seleccione una opción"
centro_seleccionado = "Seleccione una opción"

# Filtrar provincias según región
if region_seleccionada != "Seleccione una opción":
    provincias_filtradas = df3[df3['region'] == region_seleccionada]['provincia'].unique()
    provincia_opciones = ["Seleccione una opción"] + sorted(provincias_filtradas.tolist())
    provincia_seleccionada = st.sidebar.selectbox("Seleccione la provincia", options=provincia_opciones)

# Filtrar distritos según provincia
if provincia_seleccionada != "Seleccione una opción":
    distritos_filtrados = df3[(df3['region'] == region_seleccionada) & (df3['provincia'] == provincia_seleccionada)]['distrito'].unique()
    distrito_opciones = ["Seleccione una opción"] + sorted(distritos_filtrados.tolist())
    distrito_seleccionado = st.sidebar.selectbox("Seleccione el distrito", options=distrito_opciones)

# Filtrar centros de vacunación según distrito
if distrito_seleccionado != "Seleccione una opción":
    centros_filtrados = df3[(df3['region'] == region_seleccionada) & (df3['provincia'] == provincia_seleccionada) & (df3['distrito'] == distrito_seleccionado)]['Centro_vacunacion'].unique()
    centro_opciones = ["Seleccione una opción"] + sorted(centros_filtrados.tolist())
    centro_seleccionado = st.sidebar.selectbox("Seleccione el centro de vacunación", options=centro_opciones)

# Filtrar el DataFrame para obtener las coordenadas del centro de vacunación seleccionado
centro_df = df3[df3['Centro_vacunacion'] == centro_seleccionado]

# Mostrar las secciones
if centro_seleccionado != "Seleccione una opción" and not centro_df.empty:
    # Generar las secciones según la selección del usuario
    generar_grafico_barras(df3, region_seleccionada, provincia_seleccionada, distrito_seleccionado)
    generar_tabla_estadisticas(df3, region_seleccionada, provincia_seleccionada, distrito_seleccionado)
    generar_mapa_calor(df3, centro_df)
    
else:
    st.warning("Selecciona un centro de vacunación para ver la información.")



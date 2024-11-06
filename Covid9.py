import streamlit as st
import pandas as pd
import folium
import numpy as np
import plotly.express as px
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# Carga de datos
df = pd.read_csv("TB_CENTRO_VACUNACION.csv", sep=";")
df.to_csv("data.csv", sep=",")
df1 = df.copy()
df1.rename(columns={'nombre': 'Centro_vacunacion'}, inplace=True)
df1.drop(['id_centro_vacunacion', 'id_eess'], axis=1, inplace=True)
df1.replace('', np.nan, inplace=True)
df1['entidad_administra'] = df1['entidad_administra'].fillna('No especificado')

df_ubigeo = pd.read_csv("TB_UBIGEOS.csv", sep=";")
df_ubigeo.to_csv("ubigeo.csv", sep=",")
df_ub = df_ubigeo[['id_ubigeo', 'provincia', 'distrito', 'region']]
df3 = pd.merge(df1, df_ub, on='id_ubigeo', how='left')

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

# Mostrar el mapa de calor y las estadísticas
if centro_seleccionado != "Seleccione una opción" and not centro_df.empty:
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

    # Mapa de Calor
    mapa = folium.Map(location=[centro_df['latitud'].values[0], centro_df['longitud'].values[0]], zoom_start=15)
    heat_data = [[row['latitud'], row['longitud']] for index, row in df3.iterrows()]
    HeatMap(heat_data).add_to(mapa)
    st_folium(mapa, width=700, height=500)

    # Tabla dinámica con filtros
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
        st.metric(label=key, value=value)
else:
    st.warning("Selecciona un centro de vacunación para ver la información.")

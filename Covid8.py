import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import numpy as np

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

# CSS para personalizar estilo
st.markdown("""
    <style>
    .stApp {
        background-color: #f9f9f9; /* Fondo gris claro */
    }
    h1 {
        color: #2a9d8f; /* Verde suave para el título */
    }
    .css-18e3th9 {
        font-family: 'Arial', sans-serif;
        color: #264653; /* Texto principal oscuro */
    }
    .stApp iframe {
        border: 2px solid #264653; /* Color oscuro */
        box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# Configuración de título
st.title("Ubicación del Centro de Vacunación")

# Mover los selectores a una barra lateral
st.sidebar.title("Elige tu centro de vacunación")

# Agregar una opción "Seleccione una opción" al selectbox de región
region_opciones = ["Seleccione una opción"] + sorted(df3['region'].unique().tolist())
region_seleccionada = st.sidebar.selectbox("Seleccione la región", options=region_opciones)

# Variables inicializadas con valores predeterminados para evitar NameError
provincia_seleccionada = "Seleccione una opción"
distrito_seleccionado = "Seleccione una opción"
centro_seleccionado = "Seleccione una opción"

# Filtrar provincias solo si se ha seleccionado una región
if region_seleccionada != "Seleccione una opción":
    provincias_filtradas = df3[df3['region'] == region_seleccionada]['provincia'].unique()
    provincia_opciones = ["Seleccione una opción"] + sorted(provincias_filtradas.tolist())
    provincia_seleccionada = st.sidebar.selectbox("Seleccione la provincia", options=provincia_opciones)

# Filtrar distritos solo si se ha seleccionado una provincia
if provincia_seleccionada != "Seleccione una opción":
    distritos_filtrados = df3[(df3['region'] == region_seleccionada) &
                              (df3['provincia'] == provincia_seleccionada)]['distrito'].unique()
    distrito_opciones = ["Seleccione una opción"] + sorted(distritos_filtrados.tolist())
    distrito_seleccionado = st.sidebar.selectbox("Seleccione el distrito", options=distrito_opciones)

    # Filtrar centros solo si se ha seleccionado un distrito
    if distrito_seleccionado != "Seleccione una opción":
        centros_filtrados = df3[(df3['region'] == region_seleccionada) &
                                (df3['provincia'] == provincia_seleccionada) &
                                (df3['distrito'] == distrito_seleccionado)]['Centro_vacunacion'].unique()
        centro_opciones = ["Seleccione una opción"] + sorted(centros_filtrados.tolist())
        centro_seleccionado = st.sidebar.selectbox("Seleccione el centro de vacunación", options=centro_opciones)

        # Filtrar el DataFrame para obtener las coordenadas del centro de vacunación seleccionado
        centro_df = df3[df3['Centro_vacunacion'] == centro_seleccionado]

        # Verificar si centro_df está vacío antes de acceder a sus valores
        if not centro_df.empty:
            latitud = centro_df['latitud'].values[0]
            longitud = centro_df['longitud'].values[0]
            entidad_administra = centro_df['entidad_administra'].values[0]

            # Crear el mapa centrado en las coordenadas del centro seleccionado
            mapa = folium.Map(location=[latitud, longitud], zoom_start=15)

            # Agregar un marcador en la ubicación del centro de vacunación
            folium.Marker([latitud, longitud], popup=centro_seleccionado).add_to(mapa)

            # Mostrar el mapa en Streamlit
            st_folium(mapa, width=700, height=500)

            # Mostrar el nombre de la entidad administradora
            st.markdown(f"""
                <div style="background-color: #e9c46a; padding: 10px; border-radius: 5px;">
                    <h3 style="color: #264653; text-align: center;">Entidad Administradora: {entidad_administra}</h3>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No se encontraron datos para el centro de vacunación seleccionado.")

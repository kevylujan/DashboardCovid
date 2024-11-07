import plotly.express as px
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import numpy as np

# Carga de datos
df = pd.read_csv("TB_CENTRO_VACUNACION.csv", sep=";")
df1 = df.copy()
df1.rename(columns={'nombre': 'Centro_vacunacion'}, inplace=True)
df1.drop(['id_centro_vacunacion', 'id_eess'], axis=1, inplace=True)
df1.replace('', np.nan, inplace=True)
df1['entidad_administra'] = df1['entidad_administra'].fillna('No especificado')

df_ubigeo = pd.read_csv("TB_UBIGEOS.csv", sep=";")
df_ub = df_ubigeo[['id_ubigeo', 'provincia', 'distrito', 'region']]
df3 = pd.merge(df1, df_ub, on='id_ubigeo', how='left')

# Título y barra lateral
st.title("Ubicación y Estadísticas de Centros de Vacunación")
st.sidebar.title("Elige tu centro de vacunación")

# Menu de navegación
seccion = st.sidebar.radio("Selecciona la sección", ["Mapa de Calor", "Gráfico de Barras", "Tabla Dinámica y Estadísticas"])

# Funciones de cada sección
if seccion == "Mapa de Calor":
    from secciones import mapa_calor
    mapa_calor.crear_mapa(df3)

elif seccion == "Gráfico de Barras":
    from secciones import grafico_barras
    grafico_barras.crear_grafico(df3)

elif seccion == "Tabla Dinámica y Estadísticas":
    from secciones import tabla_estadisticas
    tabla_estadisticas.crear_tabla(df3)

    import folium
from streamlit_folium import st_folium
import pandas as pd

def crear_mapa(df):
    # Crear mapa centrado en una ubicación promedio
    mapa = folium.Map(location=[df['latitud'].mean(), df['longitud'].mean()], zoom_start=12)

    # Crear el mapa de calor con las coordenadas de los centros de vacunación
    from folium.plugins import HeatMap
    heat_data = [[row['latitud'], row['longitud']] for index, row in df.iterrows()]
    HeatMap(heat_data).add_to(mapa)

    # Mostrar el mapa en Streamlit
    st_folium(mapa, width=700, height=500)


def crear_grafico(df):
    # Selector para elegir el criterio de agrupación
    criterio = st.selectbox("Selecciona el criterio para el gráfico", ["Región", "Provincia", "Distrito"])
    
    # Agrupar por el criterio seleccionado y contar los centros de vacunación
    df_agrupado = df.groupby(criterio)['Centro_vacunacion'].count().reset_index()
    df_agrupado.columns = [criterio, 'Cantidad de Centros']
    
    # Crear gráfico de barras
    fig = px.bar(df_agrupado, x=criterio, y='Cantidad de Centros', title=f'Centros de Vacunación por {criterio}')
    
    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)


def crear_tabla(df):
    # Filtros de la tabla dinámica
    region = st.selectbox("Selecciona la región", df['region'].unique())
    provincia = st.selectbox("Selecciona la provincia", df[df['region'] == region]['provincia'].unique())
    distrito = st.selectbox("Selecciona el distrito", df[(df['region'] == region) & (df['provincia'] == provincia)]['distrito'].unique())
    
    # Filtrar la tabla según las opciones seleccionadas
    df_filtrado = df[(df['region'] == region) & (df['provincia'] == provincia) & (df['distrito'] == distrito)]
    
    # Mostrar tabla filtrada
    st.dataframe(df_filtrado)
    
    # Estadísticas resumidas
    st.subheader("Estadísticas Resumidas")
    st.write(f"Total de centros de vacunación en {distrito}: {df_filtrado['Centro_vacunacion'].nunique()}")
    st.write(f"Entidad Administradora más frecuente: {df_filtrado['entidad_administra'].mode()[0]}")


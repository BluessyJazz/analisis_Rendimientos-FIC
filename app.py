"""
Este script contiene el código para la aplicación web que permite analizar
las rentabilidades de los Fondos de Inversión Colectiva (FIC) en Colombia.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

# Configurar la página
st.set_page_config(page_title='Análisis de Rentabilidades de FIC',
                   page_icon='📈',
                   layout='wide',
                   initial_sidebar_state='expanded')


# Función para cargar datos desde la API
def load_data(token):
    """
    Esta función carga los datos de rentabilidades de los Fondos de Inversión
    Colectiva (FIC) desde la API de datos abiertos de Colombia.

    Args:
        token (str): Token de acceso a la API

    Returns:
        pd.DataFrame: DataFrame con los datos de rentabilidades de los FIC
    """
    url = "https://www.datos.gov.co/resource/qhpu-8ixx.json"
    headers = {"X-App-Token": token}
    response = requests.get(url, headers=headers)
    data = pd.json_normalize(response.json())
    return data


# Función para mostrar información básica
def show_data_info(df):
    """
    Esta función muestra información básica del dataset cargado.

    Args:
        df (pd.DataFrame): DataFrame con los datos de rentabilidades de los FIC

    Returns:
        None
    """

    # Mostrar información básica del dataset
    st.write("### Información General del Dataset")
    st.write(df.describe())
    st.write("### Primeras Filas del Dataset")
    st.write(df.head())


# Función para mostrar gráficos
def show_plots(df, filtro, valor_filtro):
    """
    Esta función muestra gráficas de rentabilidad promedio por entidad y
    rentabilidad en el tiempo para un valor específico del filtro seleccionado.

    Args:
        df (pd.DataFrame): DataFrame con los datos de rentabilidades de los FIC
        filtro (str): Nombre de la columna a utilizar como filtro
        valor_filtro (str): Valor del filtro seleccionado

    Returns:
        None
    """

    # Título de las gráficas
    st.write(f"### Gráficas de Rentabilidad para {filtro}: {valor_filtro}")

    # Filtrar datos según el valor del filtro seleccionado
    df_filtrado = df[df[filtro] == valor_filtro]

    # Convertir la columna FECHA_CORTE a datetime
    df_filtrado['fecha_corte'] = pd.to_datetime(df_filtrado['fecha_corte'])

    # Convertir columnas numéricas a float
    df_filtrado['rentabilidad_diaria'] = \
        df_filtrado['rentabilidad_diaria'].astype(float)

    # Gráfica de rentabilidad promedio por entidad
    avg_rentabilidad = \
        df_filtrado.groupby('nombre_entidad')['rentabilidad_diaria']
    avg_rentabilidad = avg_rentabilidad.mean().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    avg_rentabilidad.plot(kind='bar')
    plt.title('Rentabilidad Promedio por Entidad')
    plt.ylabel('Rentabilidad Promedio')
    st.pyplot(plt)

    # Gráfica de rentabilidad en el tiempo
    plt.figure(figsize=(10, 6))
    df_filtrado.groupby('fecha_corte')['rentabilidad_diaria'].mean().plot()
    plt.title('Rentabilidad Promedio en el Tiempo')
    plt.xlabel('Fecha')
    plt.ylabel('Rentabilidad Promedio')
    st.pyplot(plt)


# Función principal
def main():
    """
    Función principal que ejecuta la aplicación web.

    Args:
        None

    Returns:
        None
    """

    # Título de la aplicación
    st.title("Análisis de Rentabilidades de Fondos de Inversión \
             Colectiva (FIC)")

    # Token de la API
    api_token = "2vH90QguaeUF4e5uKL3HHb6JC"

    # Cargar datos
    data_load_state = st.text('Cargando datos...')
    data = load_data(api_token)
    data_load_state.text('Datos cargados con éxito!')

    # Convertir columnas numéricas a float
    data['rentabilidad_diaria'] = data['rentabilidad_diaria'].astype(float)

    # Mostrar información básica del dataset
    show_data_info(data)

    # Seleccionar campo para filtrar
    filtro = st.selectbox("Selecciona un campo para filtrar", data.columns)

    # Seleccionar valor del filtro
    valores_filtro = data[filtro].unique()
    valor_filtro = st.selectbox(f"Selecciona un valor \
                                para {filtro}", valores_filtro)

    # Mostrar gráficos basados en el filtro
    show_plots(data, filtro, valor_filtro)


if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd

# Título de la app
st.title('Resultados de Enero - Comparativa entre dos Clubes')

# Cargar archivo de Excel
uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel("resultado1.xlsx")

    # Mostrar el DataFrame original
    st.subheader("Datos cargados:")
    st.dataframe(df)

    # Seleccionar columna para filtrar
    columnas = df.columns.tolist()
    columna_filtro = st.selectbox("Selecciona una columna para filtrar", columnas)

    # Obtener valores únicos de la columna seleccionada
    valores_unicos = df[columna_filtro].unique()
    valor_seleccionado = st.multiselect("Selecciona valores", valores_unicos)

    # Aplicar filtro si el usuario selecciona valores
    if valor_seleccionado:
        df_filtrado = df[df[columna_filtro].isin(valor_seleccionado)]
    else:
        df_filtrado = df  # Mostrar todo si no hay filtro

    # Mostrar DataFrame filtrado
    st.subheader("Datos filtrados:")
    st.dataframe(df_filtrado)

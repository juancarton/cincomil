import streamlit as st
import pandas as pd

# Definir la contraseña
PASSWORD = "Ileana"  # Cambia esto por tu contraseña

# Widget para ingresar la contraseña
password_input = st.text_input("Ingresa la contraseña:", type="password")

if password_input == PASSWORD:
    st.success("Acceso concedido ✅")

    # Cargar archivo fijo
    try:
        df = pd.read_excel("resultado1.xlsx")  # Asegúrate de que el archivo esté en la misma carpeta
        st.subheader("Datos cargados:")
        st.dataframe(df)

        # Seleccionar columna para filtrar
        columnas = df.columns.tolist()
        columna_filtro = st.selectbox("Selecciona una columna para filtrar", columnas)

        # Obtener valores únicos de la columna seleccionada
        valores_unicos = df[columna_filtro].unique()
        valor_seleccionado = st.multiselect("Selecciona valores", valores_unicos)

        # Aplicar filtro si el usuario selecciona valores
        df_filtrado = df[df[columna_filtro].isin(valor_seleccionado)] if valor_seleccionado else df

        # Mostrar DataFrame filtrado
        st.subheader("Datos filtrados:")
        st.dataframe(df_filtrado)

    except FileNotFoundError:
        st.error("Error: No se encontró el archivo 'resultado1.xlsx'. Asegúrate de que esté en la misma carpeta.")

elif password_input:
    st.error("Contraseña incorrecta ❌")

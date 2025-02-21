import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io

# Agregar autenticación básica
PASSWORD = "Ileana"  # Cambia esto por una contraseña segura
password_input = st.text_input("🔒 Ingresa la contraseña:", type="password")

if password_input != PASSWORD:
    st.warning("Acceso denegado. Ingresa la contraseña correcta.")
    st.stop()

# URLs de los archivos en GitHub (REEMPLAZA ESTAS CON LAS CORRECTAS)
url_resultado1 = st.text_input("URL de resultado1.xlsx:")
url_categorias = st.text_input("URL de categorias.xlsx:")
url_articulos = st.text_input("URL de articulos.xlsx:")

if url_resultado1 and url_categorias and url_articulos:
    def load_excel_from_url(url):
        response = requests.get(url)
        if response.status_code == 200:
            return pd.read_excel(io.BytesIO(response.content))
        else:
            st.error(f"Error al cargar el archivo: {url}")
            return pd.DataFrame()

    # Cargar los datos desde GitHub
    resultado1_df = load_excel_from_url(url_resultado1)
    categorias_df = load_excel_from_url(url_categorias)
    articulos_df = load_excel_from_url(url_articulos)

    # Configurar la app
    st.title("📊 Comparación de Tiendas")
    st.sidebar.title("Menú de Comparación")

    opcion = st.sidebar.radio("Selecciona una opción:", [
        "Comparación de Ventas",
        "Comparación de Categorías",
        "Comparación de Artículos"
    ])

    if opcion == "Comparación de Ventas":
        st.header("📈 Comparación de Ventas entre Tiendas")
        tiendas = resultado1_df["CLUB"].unique()
        tienda1 = st.selectbox("Selecciona la primera tienda:", tiendas)
        tienda2 = st.selectbox("Selecciona la segunda tienda:", tiendas)
        
        df_filtro = resultado1_df[resultado1_df["CLUB"].isin([tienda1, tienda2])]
        st.write("### Datos Filtrados", df_filtro)
        
        fig = px.line(df_filtro, x="FECHA", y="VENTA", color="CLUB", title="Comparación de Ventas")
        st.plotly_chart(fig)

    elif opcion == "Comparación de Categorías":
        st.header("📊 Comparación por Categoría")
        categorias = categorias_df["Categoria"].unique()
        categoria = st.selectbox("Selecciona una categoría:", categorias)
        df_filtro = categorias_df[categorias_df["Categoria"] == categoria]
        
        st.write("### Datos Filtrados", df_filtro)
        fig = px.bar(df_filtro, x="CLUB", y="Venta MTD", color="CLUB", title="Venta por Categoría")
        st.plotly_chart(fig)

    elif opcion == "Comparación de Artículos":
        st.header("🛒 Comparación de Artículos Vendidos")
        articulos = articulos_df["Descripcion"].unique()
        articulo = st.selectbox("Selecciona un artículo:", articulos)
        df_filtro = articulos_df[articulos_df["Descripcion"] == articulo]
        
        st.write("### Datos Filtrados", df_filtro)
        fig = px.bar(df_filtro, x="Club", y="Actual", color="Club", title="Venta por Artículo")
        st.plotly_chart(fig)

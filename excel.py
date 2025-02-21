import streamlit as st
import pandas as pd
import plotly.express as px

# URLs de los archivos en GitHub (reemplázalas con las tuyas)
url_resultado1 = "https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/resultado1.xlsx"
url_categorias = "https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/categorias.xlsx"
url_articulos = "https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/articulos.xlsx"

# Cargar los datos desde GitHub
resultado1_df = pd.read_excel(url_resultado1)
categorias_df = pd.read_excel(url_categorias)
articulos_df = pd.read_excel(url_articulos)

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

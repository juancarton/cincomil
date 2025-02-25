import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io

# ⚠️ Mover esta línea aquí
st.set_page_config(layout="wide")

# Configuración de autenticación
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def logout():
    st.session_state.logged_in = False
    st.rerun()

PASSWORD = "Ileana"  # Cambia esto por una contraseña segura
if not st.session_state.logged_in:
    password_input = st.text_input("🔒 Ingresa la contraseña:", type="password")
    if password_input == PASSWORD:
        st.session_state.logged_in = True
        st.rerun()
    elif password_input:
        st.warning("Acceso denegado. Ingresa la contraseña correcta.")
        st.stop()
    else:
        st.stop()

# Botón de cierre de sesión
st.sidebar.button("Cerrar sesión", on_click=logout)

# URLs de los archivos en GitHub (REEMPLAZA ESTAS CON LAS CORRECTAS)
url_resultado1 = "https://raw.githubusercontent.com/juancarton/cincomil/main/resultado1.xlsx"
url_categorias = "https://raw.githubusercontent.com/juancarton/cincomil/main/categorias.xlsx"
url_articulos = "https://raw.githubusercontent.com/juancarton/cincomil/main/articulos.xlsx"

def load_excel_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        try:
            df = pd.read_excel(io.BytesIO(response.content))
            return df
        except Exception as e:
            st.error(f"Error al leer el archivo {url}: {e}")
            return pd.DataFrame()
    else:
        st.error(f"Error al cargar el archivo: {url}")
        return pd.DataFrame()

# Cargar los datos desde GitHub
resultado1_df = load_excel_from_url(url_resultado1)
categorias_df = load_excel_from_url(url_categorias)
articulos_df = load_excel_from_url(url_articulos)

# Verificar que los archivos tienen datos
if resultado1_df.empty or categorias_df.empty or articulos_df.empty:
    st.error("No se pudieron cargar correctamente los archivos. Verifica las URLs y el formato de los archivos en GitHub.")
    st.stop()

# Aplicar formato de pesos y porcentaje
def format_dataframe(df):
    if "VENTA" in df.columns:
        df["VENTA"] = df["VENTA"].apply(lambda x: f"${x:,.2f}")
    if "PLAN" in df.columns:
        df["PLAN"] = df["PLAN"].apply(lambda x: f"${x:,.2f}")
    if "ALCANCE" in df.columns:
        df["ALCANCE"] = df["ALCANCE"].apply(lambda x: f"{x:.2%}")
    return df

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
    df_filtro = format_dataframe(df_filtro)
    
    st.dataframe(df_filtro, width=1200)
    
    fig = px.line(df_filtro, x="FECHA", y="VENTA", color="CLUB", title="Comparación de Ventas")
    st.plotly_chart(fig, use_container_width=True)

elif opcion == "Comparación de Categorías":
    st.header("📊 Comparación por Categoría")
    categorias = categorias_df["Categoria"].unique()
    categoria = st.selectbox("Selecciona una categoría:", categorias)
    df_filtro = categorias_df[categorias_df["Categoria"] == categoria]
    
    df_filtro = format_dataframe(df_filtro)
    st.dataframe(df_filtro, width=1200)
    
    fig = px.bar(df_filtro, x="CLUB", y="Venta MTD", color="CLUB", title="Venta por Categoría")
    st.plotly_chart(fig, use_container_width=True)

elif opcion == "Comparación de Artículos":
    st.header("🛒 Comparación de Artículos Vendidos")
    articulos = articulos_df["Descripcion"].unique()
    articulo = st.selectbox("Selecciona un artículo:", articulos)
    df_filtro = articulos_df[articulos_df["Descripcion"] == articulo]
    
    df_filtro = format_dataframe(df_filtro)
    st.dataframe(df_filtro, width=1200)
    
    fig = px.bar(df_filtro, x="Club", y="Actual", color="Club", title="Venta por Artículo")
    st.plotly_chart(fig, use_container_width=True)

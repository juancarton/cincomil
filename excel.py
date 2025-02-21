import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io

# Configuración de autenticación
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def logout():
    st.session_state.logged_in = False
    st.rerun()

PASSWORD = "1234"  # Cambia esto por una contraseña segura
if not st.session_state.logged_in:
    password_input = st.text_input("🔒 Ingresa la contraseña:", type="password")
    if password_input == PASSWORD:
        st.session_state.logged_in = True
        st.rerun()
    else:
        st.warning("Acceso denegado. Ingresa la contraseña correcta.")
        st.stop()

# Botón de cierre de sesión
st.sidebar.button("Cerrar sesión", on_click=logout)

# URLs de los archivos en GitHub (REEMPLAZA ESTAS CON LAS CORRECTAS)
url_resultado1 = "https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/resultado1.xlsx"
url_categorias = "https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/categorias.xlsx"
url_articulos = "https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/articulos.xlsx"

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

# Asegurar que las columnas existen antes de acceder a ellas
required_columns_resultado = {"FECHA", "CLUB", "VENTA"}
required_columns_categorias = {"Categoria", "CLUB", "Venta MTD"}
required_columns_articulos = {"Descripcion", "Club", "Actual"}

if not required_columns_resultado.issubset(resultado1_df.columns):
    st.error("El archivo resultado1.xlsx no tiene las columnas esperadas. Verifica los nombres en el archivo.")
    st.stop()

if not required_columns_categorias.issubset(categorias_df.columns):
    st.error("El archivo categorias.xlsx no tiene las columnas esperadas. Verifica los nombres en el archivo.")
    st.stop()

if not required_columns_articulos.issubset(articulos_df.columns):
    st.error("El archivo articulos.xlsx no tiene las columnas esperadas. Verifica los nombres en el archivo.")
    st.stop()

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

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests

# Configuración de la página
st.set_page_config(page_title="Comparativa de Ventas", layout="wide")
st.title("📊 Comparativa de Ventas entre Club Kabah y Club Espejo")

# Autenticación con contraseña
PASSWORD = "Ileana"
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    password_input = st.text_input("🔒 Ingresa la contraseña:", type="password")
    if password_input:
        if password_input == PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("🔑 Contraseña incorrecta. Intenta de nuevo.")
            st.stop()
    else:
        st.stop()

# URLs de los archivos en GitHub
url_resultado1 = "https://raw.githubusercontent.com/juancarton/cincomil/main/resultado1.xlsx"
url_categorias = "https://raw.githubusercontent.com/juancarton/cincomil/main/categorias.xlsx"

# Función para descargar archivos
def descargar_archivo(url, nombre_local):
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        with open(nombre_local, 'wb') as archivo:
            archivo.write(respuesta.content)
        return nombre_local
    else:
        st.error(f"Error al descargar {nombre_local}: {respuesta.status_code}")
        st.stop()

# Descargar los archivos
archivo_resultado1 = descargar_archivo(url_resultado1, "resultado1.xlsx")
archivo_categorias = descargar_archivo(url_categorias, "categorias.xlsx")

# Cargar los datos de los archivos Excel
try:
    df_resultado1 = pd.read_excel(archivo_resultado1, sheet_name="Hoja1", engine='openpyxl')
    df_categorias = pd.read_excel(archivo_categorias, sheet_name="Hoja1", engine='openpyxl')
    df_resultado1["FECHA"] = pd.to_datetime(df_resultado1["FECHA"])
except Exception as e:
    st.error(f"⚠️ Error al cargar los archivos: {e}")
    st.stop()

# Sidebar con filtros
st.sidebar.header("📅 Filtros")
fecha_min, fecha_max = df_resultado1["FECHA"].min(), df_resultado1["FECHA"].max()
fecha_seleccionada = st.sidebar.date_input("Selecciona un rango de fechas", [fecha_min, fecha_max], fecha_min, fecha_max)
dias_seleccionados = st.sidebar.multiselect("Selecciona días de la semana", df_resultado1["DIA"].unique(), df_resultado1["DIA"].unique())
categorias_seleccionadas = st.sidebar.multiselect("Selecciona Categorías", df_categorias["Categoria"].unique(), df_categorias["Categoria"].unique())

# Filtrar datos según selección
df_filtrado = df_resultado1[
    (df_resultado1["FECHA"] >= pd.to_datetime(fecha_seleccionada[0])) &
    (df_resultado1["FECHA"] <= pd.to_datetime(fecha_seleccionada[1])) &
    (df_resultado1["DIA"].isin(dias_seleccionados))
]

# 📋 Mostrar tabla de datos
tab1, tab2, tab3 = st.tabs(["📊 Ventas", "📋 Categorías", "📋 Resultado1"])

with tab1:
    st.subheader("📊 Comparación General de Ventas")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=df_filtrado, x="CLUB", y="VENTA", palette="viridis", ax=ax)
    ax.set_title("Comparación de Ventas entre Tiendas")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, fontsize=9)
    st.pyplot(fig)

    # 📈 Comparación de tendencias con línea
    st.subheader("📈 Tendencias de Ventas en el Tiempo")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.lineplot(data=df_filtrado, x="FECHA", y="VENTA", hue="CLUB", marker="o", ax=ax)
    ax.set_title("Tendencia de Ventas por Día")
    st.pyplot(fig)

with tab2:
    st.subheader("📋 Tabla de Categorías")
    st.dataframe(df_categorias)

    # 📊 Comparación de categorías con Seaborn (corregida)
    df_categorias_filtrado = df_categorias[df_categorias["Categoria"].isin(categorias_seleccionadas)]
    if not df_categorias_filtrado.empty:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=df_categorias_filtrado, x="CLUB", y="Venta MTD", hue="Categoria", palette="coolwarm", ax=ax)
        ax.set_title("Comparación de Ventas MTD por Categoría")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=30, fontsize=9)
        st.pyplot(fig)

with tab3:
    st.subheader("📋 Tabla de Resultado1")
    st.dataframe(df_resultado1)

# Botón de cierre de sesión
if st.button("Cerrar Sesión"):
    st.session_state["authenticated"] = False
    st.rerun()

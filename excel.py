import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Comparativa de Ventas", layout="wide")
st.title("📊 Comparativa de Ventas entre Club Kabah y Club Espejo")

# Autenticación con contraseña
PASSWORD = "Ileana"  # Contraseña fija
temp_password = st.session_state.get("authenticated", False)
password_input = st.text_input("🔒 Ingresa la contraseña:", type="password")

if password_input == PASSWORD or temp_password:
    st.session_state["authenticated"] = True
    
    # Cargar datos de los archivos Excel con manejo de errores
    resultado1_path = "/mnt/data/resultado1.xlsx"
    categorias_path = "/mnt/data/categorias.xlsx"
    
    try:
        df_resultado1 = pd.read_excel(resultado1_path, sheet_name="Hoja1", engine='openpyxl')
        df_categorias = pd.read_excel(categorias_path, sheet_name="Hoja1", engine='openpyxl')
        df_resultado1["FECHA"] = pd.to_datetime(df_resultado1["FECHA"])
    except Exception as e:
        st.error(f"⚠️ Error al cargar los archivos: {e}")
        st.stop()
    
    # Sidebar con filtros
    st.sidebar.header("📅 Filtros")
    fecha_min, fecha_max = df_resultado1["FECHA"].min(), df_resultado1["FECHA"].max()
    fecha_seleccionada = st.sidebar.date_input("Selecciona un rango de fechas", [fecha_min, fecha_max], fecha_min, fecha_max)
    dias_seleccionados = st.sidebar.multiselect("Selecciona días de la semana", df_resultado1["DIA"].unique(), df_resultado1["DIA"].unique())
    
    # Filtrar datos según selección
    df_filtrado = df_resultado1[
        (df_resultado1["FECHA"] >= pd.to_datetime(fecha_seleccionada[0])) &
        (df_resultado1["FECHA"] <= pd.to_datetime(fecha_seleccionada[1])) &
        (df_resultado1["DIA"].isin(dias_seleccionados))
    ]
    
    # 📊 Comparación de ventas con gráfica de barras (siempre visible)
    st.subheader("📊 Comparación General de Ventas")
    fig = px.bar(df_filtrado, x="CLUB", y="VENTA", color="CLUB", title="Comparación de Ventas entre Tiendas")
    st.plotly_chart(fig, use_container_width=True)
    
    # 📈 Comparación de tendencias con línea
    st.subheader("📈 Tendencias de Ventas en el Tiempo")
    fig = px.line(df_filtrado, x="FECHA", y="VENTA", color="CLUB", markers=True, title="Tendencia de Ventas por Día")
    st.plotly_chart(fig, use_container_width=True)
    
    # 📊 Comparación de categorías
    st.subheader("📊 Comparación de Ventas por Categoría")
    categoria_seleccionada = st.sidebar.selectbox("Selecciona una Categoría", df_categorias["Categoria"].unique())
    df_categoria_filtrado = df_categorias[df_categorias["Categoria"] == categoria_seleccionada]
    
    fig = px.bar(df_categoria_filtrado, x="CLUB", y="Venta MTD", color="CLUB", title=f"Venta MTD por Categoría: {categoria_seleccionada}")
    st.plotly_chart(fig, use_container_width=True)
    
    # Botón de cierre de sesión
    if st.button("Cerrar Sesión"):
        st.session_state["authenticated"] = False
        st.experimental_rerun()
else:
    st.error("🔑 Contraseña incorrecta. Intenta de nuevo.")

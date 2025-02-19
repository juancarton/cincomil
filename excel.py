import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Comparativa entre el Club Kabah y su Club Espejo", layout="wide")
st.title("📊 Comparativa entre el Club Kabah y su Club Espejo")

# Autenticación con contraseña
PASSWORD = "Ileana"  # Cambiar por la contraseña deseada
password_input = st.text_input("🔒 Ingresa la contraseña:", type="password")

if password_input == PASSWORD:
    # Cargar archivo Excel
    uploaded_file = st.file_uploader("Sube un archivo Excel con los datos", type=["xlsx"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file, sheet_name="Hoja1")
        
        # Asegurar que las columnas necesarias estén presentes
        required_columns = ["FECHA", "DIA", "CLUB", "VENTA", "PLAN", "DEC/CREC", "ALCANCE", "TRANSACCIONES"]
        if all(col in df.columns for col in required_columns):
            
            # Convertir fecha a datetime para filtros
            df["FECHA"] = pd.to_datetime(df["FECHA"])
            
            # Filtros de fecha y día
            st.sidebar.header("📅 Filtros")
            fecha_min, fecha_max = df["FECHA"].min(), df["FECHA"].max()
            fecha_seleccionada = st.sidebar.date_input("Selecciona un rango de fechas", [fecha_min, fecha_max], fecha_min, fecha_max)
            dias_seleccionados = st.sidebar.multiselect("Selecciona días de la semana", df["DIA"].unique(), df["DIA"].unique())
            
            df_filtrado = df[(df["FECHA"] >= pd.to_datetime(fecha_seleccionada[0])) & (df["FECHA"] <= pd.to_datetime(fecha_seleccionada[1])) & df["DIA"].isin(dias_seleccionados)]
            
            # Mostrar la tabla con estilos
            st.subheader("📋 Datos de Ventas y Transacciones")
            st.dataframe(df_filtrado.style.format({"VENTA": "${:,.2f}", "TRANSACCIONES": "{:,}", "PLAN": "${:,.2f}", "DEC/CREC": "{:.1f}%", "ALCANCE": "{:.2f}"}))
            
            # Gráficos
            st.subheader("📊 Comparación de Ventas")
            fig_ventas = px.bar(df_filtrado, x="CLUB", y="VENTA", color="CLUB", text_auto=True,
                                title="Comparación de Ventas entre Tiendas")
            st.plotly_chart(fig_ventas, use_container_width=True)
            
            st.subheader("📈 Comparación de Transacciones")
            fig_transacciones = px.bar(df_filtrado, x="CLUB", y="TRANSACCIONES", color="CLUB", text_auto=True,
                                       title="Comparación de Transacciones entre Tiendas")
            st.plotly_chart(fig_transacciones, use_container_width=True)
            
            # Relación Ventas/Transacciones
            df_filtrado["Ventas por Transacción"] = df_filtrado["VENTA"] / df_filtrado["TRANSACCIONES"]
            st.subheader("💰 Promedio de Ventas por Transacción")
            fig_ratio = px.bar(df_filtrado, x="CLUB", y="Ventas por Transacción", color="CLUB", text_auto=True,
                               title="Promedio de Ventas por Transacción")
            st.plotly_chart(fig_ratio, use_container_width=True)
        else:
            st.error(f"El archivo debe contener las columnas: {', '.join(required_columns)}")
    else:
        st.info("📂 Sube un archivo Excel para comenzar")
else:
    st.error("🔑 Contraseña incorrecta. Intenta de nuevo.")

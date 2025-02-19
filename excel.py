import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Comparativa entre el Club Kabah y su Club Espejo", layout="wide")
st.title("📊 Comparativa entre el Club Kabah y su Club Espejo")

# Autenticación con contraseña
PASSWORD = "Ileana"  # Cambiar por la contraseña deseada
password_input = st.text_input("🔒 Ingresa la contraseña:", type="password")

if password_input == PASSWORD:
    # Cargar archivo fijo
    file_path = "resultado1.xlsx"

    try:
        df = pd.read_excel(file_path, sheet_name="Hoja1")
        
        # Verificar si las columnas requeridas existen
        required_columns = ["FECHA", "DIA", "CLUB", "VENTA", "PLAN", "DEC/CREC", "ALCANCE", "TRANSACCIONES"]
        if all(col in df.columns for col in required_columns):
            
            # Convertir fecha a datetime para filtros
            df["FECHA"] = pd.to_datetime(df["FECHA"])
            
            # Sidebar con filtros
            st.sidebar.header("📅 Filtros")
            fecha_min, fecha_max = df["FECHA"].min(), df["FECHA"].max()
            fecha_seleccionada = st.sidebar.date_input("Selecciona un rango de fechas", [fecha_min, fecha_max], fecha_min, fecha_max)
            dias_seleccionados = st.sidebar.multiselect("Selecciona días de la semana", df["DIA"].unique(), df["DIA"].unique())

            # Filtrar datos
            df_filtrado = df[
                (df["FECHA"] >= pd.to_datetime(fecha_seleccionada[0])) & 
                (df["FECHA"] <= pd.to_datetime(fecha_seleccionada[1])) & 
                (df["DIA"].isin(dias_seleccionados))
            ]
            
            # Mostrar la tabla con estilos
            st.subheader("📋 Datos de Ventas y Transacciones")
            st.dataframe(df_filtrado.style.format({"VENTA": "${:,.2f}", "TRANSACCIONES": "{:,}", "PLAN": "${:,.2f}", "DEC/CREC": "{:.1f}%", "ALCANCE": "{:.2f}"}))

            # Crear diseño en columnas para evitar scroll
            col1, col2 = st.columns(2)

            # Gráfico de ventas
            with col1:
                st.subheader("📊 Comparación de Ventas")
                fig, ax = plt.subplots(figsize=(8, 5))
                sns.barplot(data=df_filtrado, x="CLUB", y="VENTA", palette="viridis", ax=ax)
                ax.set_title("Comparación de Ventas entre Tiendas")
                ax.set_ylabel("Ventas ($)")
                ax.set_xlabel("Club")
                st.pyplot(fig)

            # Gráfico de transacciones
            with col2:
                st.subheader("📈 Comparación de Transacciones")
                fig, ax = plt.subplots(figsize=(8, 5))
                sns.barplot(data=df_filtrado, x="CLUB", y="TRANSACCIONES", palette="coolwarm", ax=ax)
                ax.set_title("Comparación de Transacciones entre Tiendas")
                ax.set_ylabel("Número de Transacciones")
                ax.set_xlabel("Club")
                st.pyplot(fig)

            # Relación Ventas/Transacciones en una fila separada
            st.subheader("💰 Promedio de Ventas por Transacción")
            df_filtrado["Ventas por Transacción"] = df_filtrado["VENTA"] / df_filtrado["TRANSACCIONES"]
            
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.bar

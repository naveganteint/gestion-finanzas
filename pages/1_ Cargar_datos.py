import streamlit as st
import pandas as pd
import numpy as np
from styles.estilos import aplicar_estilos

aplicar_estilos()

# Título
st.markdown(
    "<h1 style='color:#2E3A59;'>Cargar archivo Excel</h1>",
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Selecciona tu archivo Excel",
    type=["xlsx"]
)

# Inicializar session_state
if "hojas" not in st.session_state:
    st.session_state.hojas = {}

if uploaded_file:

    try:
        xls = pd.ExcelFile(uploaded_file)

        st.write("📄 Hojas detectadas en el archivo las siguientes pestañas:", xls.sheet_names)

        # hojas que queremos
        hojas_objetivo = ["datos", "patrones"]

        cargadas = 0

        for hoja in hojas_objetivo:

            if hoja in xls.sheet_names:

                df = xls.parse(hoja)

                # 🔧 limpieza de datos
                df.columns = df.columns.map(str)
                df.columns = df.columns.astype(str).str.strip()
                df = df.replace(['—', '-', ''], np.nan)
                df = df.infer_objects()

                df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

                st.session_state.hojas[hoja] = df
                cargadas += 1
    

            else:
                st.warning(f"⚠️ La hoja '{hoja}' no existe en el archivo")

        if cargadas > 0:
            st.success(f"✅ Se cargaron las {cargadas} hojas necesarias correctamente:&nbsp;&nbsp; '{', '.join(st.session_state.hojas.keys())}'")



        else:
            st.error("❌ No se cargó ninguna hoja válida")

    except Exception as e:
        st.error(f"Error al leer el Excel: {e}")
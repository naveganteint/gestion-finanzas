import streamlit as st
import numpy as np
from styles.estilos import aplicar_estilos

aplicar_estilos()

st.markdown("<h1 style='color:#2E3A59'>Ver datos</h1>", unsafe_allow_html=True)


st.write("")

if "hojas" in st.session_state and "patrones" in st.session_state.hojas:

    df = st.session_state.hojas["patrones"]

    st.markdown(
        '<h3 style="color: #2E3A59; background-color: #C2DAC1; padding: 5px; border-radius: 5px;">Tabla: patrones</h3>',
        unsafe_allow_html=True
    )

    st.write("")
    df_limpio = df.copy()

    df_limpio.columns = df_limpio.columns.map(str)

    df_limpio.replace('—', np.nan, inplace=True)
    df_limpio = df_limpio.infer_objects()

    df_mostrar = df_limpio.astype(str).replace("nan", "-")

    st.table(df_mostrar)

else:
    st.info("Primero carga un archivo en 'Cargar Excel' o no existe la hoja 'patrones'")


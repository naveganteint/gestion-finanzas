import streamlit as st
import pandas as pd
import datetime
from styles.estilos import aplicar_estilos,h3_especial,h2_especial
import utils.funciones as ut

aplicar_estilos()


st.markdown(
    "<h1 style='color:#2E3A59; text-align:center;'>Control Mensual</h1>",
    unsafe_allow_html=True
)


# =========================================================
# 🔍 COMPROBAR DATOS
# =========================================================
if (
    "hojas" in st.session_state and
    "datos" in st.session_state.hojas and
    "patrones" in st.session_state.hojas
):

    # =====================================================
    # 📊 DATOS PRINCIPALES
    # =====================================================
    df_datos = st.session_state.hojas["datos"].copy()

    # 🔧 limpieza año (SIN afectar original)
    df_datos["AÑO"] = pd.to_numeric(df_datos["AÑO"], errors="coerce")
    df_datos = df_datos.dropna(subset=["AÑO"])
    df_datos["AÑO"] = df_datos["AÑO"].astype(int)

    # 📌 lista de años
    anios = sorted(df_datos["AÑO"].unique().tolist())

    # 📅 año actual
    anio_actual = datetime.datetime.now().year

    # 🧠 default seguro
    default_year = anio_actual if anio_actual in anios else anios[-1]
    default_index = anios.index(default_year)

    # 📥 selector centrado
    col1, col2, col3 = st.columns([1, 1, 4])

    with col2:
        anio_seleccionado = st.selectbox(
            "Selecciona el año",
            anios,
            index=default_index
        )

    h3_especial("Ingresos")    
    st.write("")

    # =====================================================
    # 📌 PATRONES (SEPARADO Y SEGURO)
    # =====================================================
    df_patrones = st.session_state.hojas["patrones"].copy()

    df_patrones.columns = df_patrones.columns.map(str)

  

    



    # validar que existan al menos 5 columnas
    if df_patrones.shape[1] >= 5:

        companias = df_patrones["compañias"].iloc[0:].dropna().astype(str).tolist()
        otros_ingresos = df_patrones["otros ingresos"].iloc[0:].dropna().astype(str).tolist()
        recursos_humanos = df_patrones["Recursos Humanos"].iloc[0:].dropna().astype(str).tolist()
        suministros = df_patrones["Suministros"].iloc[0:].dropna().astype(str).tolist()
        servicios = df_patrones["Servicios"].iloc[0:].dropna().astype(str).tolist()
        local = df_patrones["local"].iloc[0:].dropna().astype(str).tolist()
        




#********************************* ESPACIO PARA VISUALIZAR LOS DATOS ************************************************


        h2_especial("Compañias","white")
        datos_filtrados= ut.tabla_filtro(df_datos, anio_seleccionado, companias) 
        ultima_fila1 = datos_filtrados.iloc[-1]
        ut.mostrar_tabla(datos_filtrados)
                


        h2_especial("Otros Ingresos","white")
        datos_filtrados= ut.tabla_filtro(df_datos, anio_seleccionado, otros_ingresos) 
        ultima_fila2 = datos_filtrados.iloc[-1]
        ut.mostrar_tabla(datos_filtrados)

        h2_especial("Total Ingresos")  
        encabezado = datos_filtrados.columns.tolist()    
        encabezado.insert(0, "")
        encabezado[-1] = ""
         
        total_ingresos=ut.suma_listas (ultima_fila1,ultima_fila2)
        ut.mostrar_dos_arrays_texto(encabezado, total_ingresos ,"Total ingresos")

        st.write("")
        h3_especial("Gastos","#ffb3b3")    
        st.write("")
            
        h2_especial("Suministros","white") 
        datos_filtrados= ut.tabla_filtro(df_datos, anio_seleccionado, suministros) 
        ultima_fila3 = datos_filtrados.iloc[-1]
        ut.mostrar_tabla(datos_filtrados,"#ffe6e6","tabla_2")


        h2_especial("Recursos Humanos","white") 
        datos_filtrados= ut.tabla_filtro(df_datos, anio_seleccionado, recursos_humanos) 
        ultima_fila4 = datos_filtrados.iloc[-1]
        ut.mostrar_tabla(datos_filtrados,"#ffe6e6","tabla_2")

        h2_especial("Servicios","white") 
        datos_filtrados= ut.tabla_filtro(df_datos, anio_seleccionado, servicios) 
        ultima_fila5 = datos_filtrados.iloc[-1]
        ut.mostrar_tabla(datos_filtrados,"#ffe6e6","tabla_2")


        h2_especial("Local","white") 
        datos_filtrados= ut.tabla_filtro(df_datos, anio_seleccionado, local) 
        ultima_fila6 = datos_filtrados.iloc[-1]
        ut.mostrar_tabla(datos_filtrados,"#ffe6ff","tabla_2")


        h2_especial("Total Gastos","#ffb3b3")  
         
        total_gastos=ut.suma_listas (ultima_fila3,ultima_fila4)
        total_gastos=ut.suma_listas (total_gastos,ultima_fila5)
        total_gastos=ut.suma_listas (total_gastos,ultima_fila6)

        ut.mostrar_dos_arrays_texto(encabezado, total_gastos ,"Total Gastos")


        h3_especial("Resultado","#e6b7f8")  
        

        resultado=ut.suma_listas (total_ingresos,total_gastos)
        ut.mostrar_dos_arrays_texto(encabezado, resultado ,"Resultado")

        st.write("")
        st.write("")

        h3_especial("Patrones no utilizados en el año","#959296")  

        patrones_año= ut.busca_patrones_año(df_datos, anio_seleccionado)
        patrones=ut.recopila_patrones(df_patrones)

     

        patrones_no_incluidos=ut.elementos_no_incluidos(patrones_año, patrones)
        st.write("")
        st.markdown(
        f"""
        <p style="font-size:20px;color: #1b3865;">
            {' //  '.join(map(str, patrones_no_incluidos))}
        </p>
        """,
        unsafe_allow_html=True
)













#*************************************** FIN ESPACIO PARA VISUALIZAR LOS DATOS****************************************************************************
    else:
        st.warning("La hoja 'patrones' no tiene suficientes columnas")



else:
    st.warning("⚠️ Primero carga los datos en el Excel")
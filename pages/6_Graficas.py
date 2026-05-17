import streamlit as st
import pandas as pd
from styles.estilos import aplicar_estilos,h3_especial,h2_especial
import utils.funciones as ut
import utils.plots as pl
aplicar_estilos()
import numpy as np

st.markdown(
    "<h1 style='color:#2E3A59; text-align:center;'>Graficas</h1>",
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

    # 📌 lista de años (slider)


    anios_disponibles = sorted(df_datos["AÑO"].dropna().unique().tolist())


    # 🔲 ESTILO GLOBAL DEL BLOQUE DEL SLIDER
    st.markdown("""
    <style>

    /* 🔥 Contenedor real de las columnas */
    div[data-testid="stHorizontalBlock"] {
        border: 2px solid #999;
        background-color: #f5f7f7;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
        width:60%;
        margin: 0 auto 15px auto;  /* 👈 CENTRADO REAL */               
    }

    /* 🎨 Slider (opcional mejora visual) Punto para marcar años en el slider*/
    div[data-baseweb="slider"] div[role="slider"] {
        background-color: #8AA1C1 !important;
    }

    /* barra completa */
    div[data-baseweb="slider"] {
        --slider-progress-background: purple;
    }

    /* handle */
    div[data-baseweb="slider"] div[role="slider"] {
        background-color: #8AA1C1 !important;
        border: 2px solid white;
    }

    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 9, 1])

    with col2:
            rango_años = st.slider(
                "Selecciona rango de años",
                min_value=min(anios_disponibles),
                max_value=max(anios_disponibles),
                value=(min(anios_disponibles), max(anios_disponibles))
            )


                

    st.write("")
    st.write("")    
    anios = list(range(rango_años[0], rango_años[1] + 1))










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

        #++++++++++++++++++++++++++++++++++++++++++++ Grafica de Ingresos y Gastos por año ++++++++++++++++++++++++++++++++++++

        h3_especial("Grafica de Ingresos y Gastos por año") 


        lista_ingresos = companias+otros_ingresos
        lista_gastos=recursos_humanos+suministros+servicios+local

        ingresos=ut.suma_positivos_por_anio(df_datos, anios,lista_ingresos) 
        gastos=ut.suma_negativos_por_anio(df_datos, anios,lista_gastos)
        gastos1 = [-x for x in gastos]
        
        resultado=ut.suma_listas(ingresos,gastos)

        pl.graficar_tres_lineas(ingresos, gastos1, resultado,"#11C21A","#EE1414","#A008A5", eje_x=anios, etiquetas=("Ingresos","Gastos","Resultado"), eje_y="Euros")


        
                #************************************************ Grafica de Ingresos por años ************************************

        h3_especial("Grafica de Ingresos por años") 
        st.write("")

        grupos3 = lista_ingresos
        compañias=df_patrones["compañias"].iloc[0:].dropna().astype(str).tolist()
        
        opciones_grupo = ["TODOS","Compañias"] + grupos3

        col1, col2, col3 = st.columns([1, 1, 4])

        with col2:
            grupo_seleccionado = st.selectbox(
                "Selecciona el grupo",
                opciones_grupo,
                index=0,
                key="select_ingresos_años"
            )

        if grupo_seleccionado == "TODOS":
            lista_grupos_filtrados = grupos3

        elif grupo_seleccionado == "Compañias":
            lista_grupos_filtrados = companias  # 👈 aquí usas la lista

        else:
            lista_grupos_filtrados = [grupo_seleccionado]

        ingresos =ut.suma_positivos_por_año_grupo (df_datos, anios,lista_grupos_filtrados)

        
        pl.grafica_columnas(anios, ingresos,"Años","Ingresos","#37819E")

    

        h3_especial("Grafica de Gastos por años") 
        st.write("")

        grupos4 = lista_gastos
        
        opciones_grupo = ["TODOS"] + grupos4

        col1, col2, col3 = st.columns([1, 1, 4])

        with col2:
            grupo_seleccionado = st.selectbox(
                "Selecciona el grupo",
                opciones_grupo,
                index=0,
                key="select_gastos_años"
            )

        if grupo_seleccionado == "TODOS":
            lista_grupos_filtrados = grupos4

        else:
            lista_grupos_filtrados = [grupo_seleccionado]

        gastos =ut.suma_negativos_por_año_grupo (df_datos, anios,lista_grupos_filtrados)
        gastos= [-x for x in gastos]
        
        pl.grafica_columnas(anios, gastos,"Años","Gastos","#F5615C")














        #++++++++++++++++++++++++++++++++++++++++++++ Grafica de Ingresos por mes++++++++++++++++++++++++++++++++++++

        h3_especial("Grafica de Ingresos  por  mes") 
        st.write("")
        
        grupos = lista_ingresos

        opciones_grupo = ["TODOS"] + grupos

        col1, col2, col3 = st.columns([1, 1, 4])

        with col2:
            grupo_seleccionado = st.selectbox(
                "Selecciona el grupo",
                opciones_grupo,
                index=0,
                key="select_ingresos_mes"
            )

        if grupo_seleccionado == "TODOS":
            lista_grupos_filtrados = grupos
        else:
            lista_grupos_filtrados = [grupo_seleccionado]




        lista_meses=[1,2,3,4,5,6,7,8,9,10,11,12]


        ingresos, labels =ut.suma_positivos_por_anio_mes(df_datos, anios,lista_meses,lista_grupos_filtrados)
   

        pl.grafica_columnas(labels, ingresos,"Meses","Ingresos","#37819E")


        st.write("")
        st.write("")

        ingresos, labels =ut.suma_positivos_por_anio_mes2 (df_datos, anios,lista_meses,lista_grupos_filtrados)
   

        pl.grafica_columnas_agrupadas(labels, ingresos,"Meses","Ingresos")

        #************************************************ Graficas de  gastos ************************************

        h3_especial("Grafica de Gastos  por  mes") 
        st.write("")
        
        grupos2 = lista_gastos

        opciones_grupo = ["TODOS"] + grupos2

        col1, col2, col3 = st.columns([1, 1, 4])

        with col2:
            grupo_seleccionado = st.selectbox(
                "Selecciona el grupo",
                opciones_grupo,
                index=0,
                key="select_gastos_mes"
            )

        if grupo_seleccionado == "TODOS":
            lista_grupos_filtrados = grupos2
        else:
            lista_grupos_filtrados = [grupo_seleccionado]


        print (lista_grupos_filtrados)

        lista_meses=[1,2,3,4,5,6,7,8,9,10,11,12]


        gastos, labels =ut.suma_negativos_por_anio_mes(df_datos, anios,lista_meses,lista_grupos_filtrados)
   
        gastos= [-x for x in gastos]


        pl.grafica_columnas(labels, gastos,"Meses","Gastos","#EE6662")


        st.write("")
        st.write("")

        gastos, labels =ut.suma_negativos_por_anio_mes2 (df_datos, anios,lista_meses,lista_grupos_filtrados)
        gastos= [-x for x in gastos]

        pl.grafica_columnas_agrupadas(labels, gastos,"Meses","Gastos")











        



























#*************************************** FIN ESPACIO PARA VISUALIZAR LOS DATOS****************************************************************************
    else:
        st.warning("La hoja 'patrones' no tiene suficientes columnas")



else:
    st.warning("⚠️ Primero carga los datos en el Excel")


   
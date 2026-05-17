import numpy as np
import streamlit as st
import pandas as pd
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import re






#**************************************************************************************
    #************************ graficar tres lineas ***********************************
#**************************************************************************************


def graficar_tres_lineas(lista1, lista2, lista3,color1,color2,color3, eje_x=None, etiquetas=None, eje_y="margenes %"):
        """
        Genera una gráfica de líneas con tres listas de valores usando Matplotlib y la muestra en Streamlit.
        
        Parámetros:
        - lista1, lista2, lista3: listas de valores numéricos (misma longitud)
        - eje_x: lista de valores para el eje X (por ejemplo años). Por defecto 1..n
        - etiquetas: lista de 3 strings para la leyenda de cada línea (opcional)
        - titulo: título de la gráfica
        - eje_y: nombre del eje Y (por defecto "Valores")
        """
        # Validar longitud
        n = len(lista1)
        if len(lista2) != n or len(lista3) != n:
            raise ValueError("Todas las listas deben tener la misma longitud")
        
        # Eje X por defecto
        if eje_x is None:
            eje_x = list(range(1, n+1))
        
        if len(eje_x) != n:
            raise ValueError("La lista del eje X debe tener la misma longitud que las listas de valores")
        
        # Etiquetas por defecto
        if etiquetas is None:
            etiquetas = ["Línea 1", "Línea 2", "Línea 3"]
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(7,4))                             
        
        # Graficar líneas
        ax.plot(eje_x, lista1,  label=etiquetas[0], color=color1)
        ax.plot(eje_x, lista2,  label=etiquetas[1], color=color2)
        ax.plot(eje_x, lista3,  label=etiquetas[2], color=color3)
        

        # Eliminar todos los spines (bordes de la gráfica)
        for spine in ax.spines.values():
            spine.set_visible(False)


        # Títulos y etiquetas
        #ax.set_title(titulo, fontsize=14)
        ax.set_xlabel("Año" if eje_x else "Índice", fontsize=12, color='gray')
        ax.set_ylabel(eje_y, fontsize=12, color='gray')

        
        ax.tick_params(axis='x', colors='gray', length=5, width=1)  # ticks eje X
        ax.tick_params(axis='y', colors='gray', length=5, width=1)  # ticks eje Y

        
        # Leyenda y cuadrícula
        ax.legend()
     
        
        ax.yaxis.grid(True, color='gray', linestyle='-', linewidth=1)  # gris claro y punteado
        ax.axhline(y=0, color='black', linewidth=2, linestyle='-')

        plt.tight_layout()
        
        
        # Guardar figura en buffer
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight')  # bbox_inches evita recorte de etiquetas
        buf.seek(0)

        # Convertir a base64 para incrustar en HTML
        img_base64 = base64.b64encode(buf.read()).decode()

        # HTML para centrar imagen con ancho fijo de 700px
        st.markdown(f"""
        <div style="display:flex; justify-content:center;">
            <img src="data:image/png;base64,{img_base64}" width="700px">
        </div>
        """, unsafe_allow_html=True)



#**************************************************************************************
    #************************ grafica barras por meses ***********************************
#**************************************************************************************




def grafica_columnas(arr1, arr2, eje_x, eje_y, color_barras):
    
    df = pd.DataFrame({'x': arr1, 'y': arr2})

    # 📊 figura más grande (dashboard)
    fig, ax = plt.subplots(figsize=(20, 10))

    ax.bar(df['x'], df['y'], color=color_barras)

    # 📌 etiquetas de ejes
    ax.set_xlabel(eje_x, color='gray', fontsize=16, labelpad=15)
    ax.set_ylabel(eje_y, color='gray', fontsize=18, labelpad=15)

    # 🔢 ticks base (se sobrescribe luego)
    ax.set_xticks(df['x'])

    # 🎯 estilo ticks eje X e Y
    ax.tick_params(axis='x', colors='black', labelsize=14, rotation=45)
    ax.tick_params(axis='y', colors='black', labelsize=20)

    # 📈 grid
    ax.yaxis.grid(True, color='gray', linestyle='-', linewidth=1)
    ax.set_axisbelow(True)

    # 🧠 reducir saturación eje X
    step = max(1, len(df['x']) // 12)
    ax.set_xticks(df['x'][::step])
    ax.set_xticklabels(df['x'][::step], fontsize=16, rotation=45, ha='right')

    # 🧹 eliminar bordes
    for spine in ax.spines.values():
        spine.set_visible(False)

    # 📏 ajustar layout
    fig.tight_layout()

    # 💾 guardar imagen
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)

    img_base64 = base64.b64encode(buf.read()).decode()

    # 📊 mostrar en Streamlit centrado
    st.markdown(f"""
    <div style="display:flex; justify-content:center;">
        <img src="data:image/png;base64,{img_base64}" width="900px">
    </div>
    """, unsafe_allow_html=True)


#**************************************************************************************
    #************************ graficar barras por mes ordenados  ***********************************
#**************************************************************************************







def grafica_columnas_agrupadas(arr1, arr2, eje_x, eje_y):


        df = pd.DataFrame({'x': arr1, 'y': arr2})

        # 📊 figura más grande (dashboard)
        fig, ax = plt.subplots(figsize=(20, 10))

        # ----------------------------------------------------
        # 🎨 COLORES POR MES
        # ----------------------------------------------------
        # asumimos formato "01-2020"
        meses_unicos = sorted(set([x.split("-")[0] for x in arr1]))

        colores_mes = {
            mes: plt.cm.tab20(i % 20)
            for i, mes in enumerate(meses_unicos)
        }

        colores = [colores_mes[x.split("-")[0]] for x in arr1]

        # 📊 barra con colores por mes
        ax.bar(df['x'], df['y'], color=colores)

        # 📌 etiquetas de ejes
        ax.set_xlabel(eje_x, color='gray', fontsize=16, labelpad=15)
        ax.set_ylabel(eje_y, color='gray', fontsize=18, labelpad=15)

        # 🔢 ticks base
        ax.set_xticks(df['x'])

        # 🎯 estilo ticks
        ax.tick_params(axis='x', colors='black', labelsize=20, pad=20)
        ax.tick_params(axis='y', colors='black', labelsize=20)

        # 📈 grid
        ax.yaxis.grid(True, color='gray', linestyle='-', linewidth=1)
        ax.set_axisbelow(True)

        # 🧠 reducir saturación eje X
        step = max(1, len(df['x']) // 12)

        x = np.arange(len(df['x']))
        ax.bar(x, df['y'], color=colores)

        df_temp = pd.DataFrame({"x": df['x'], "pos": x})
        df_temp["mes"] = df_temp["x"].str.split("-").str[0]

        centros = df_temp.groupby("mes")["pos"].mean()

        ax.set_xticks(centros.values)
        ax.set_xticklabels(centros.index, fontsize=20, ha='center')

        # 🧹 eliminar bordes
        for spine in ax.spines.values():
            spine.set_visible(False)

        # 📏 ajustar layout
        fig.tight_layout()

        # 💾 guardar imagen
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight')
        buf.seek(0)

        img_base64 = base64.b64encode(buf.read()).decode()

        # 📊 mostrar en Streamlit centrado
        st.markdown(f"""
        <div style="display:flex; justify-content:center;">
            <img src="data:image/png;base64,{img_base64}" width="900px">
        </div>
        """, unsafe_allow_html=True)



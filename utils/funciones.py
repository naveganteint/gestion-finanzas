import pandas as pd
import streamlit as st

def tabla_filtro(df_datos, anio_seleccionado, companias):

    df = df_datos.copy()
 










    # 🧹 limpiar columnas innecesarias
    df = df.drop(columns=["F.Valor", "Disponible", "Observaciones", "Movimiento"])

    # 🔧 MES seguro
    df["MES"] = pd.to_numeric(df["MES"], errors="coerce")
    df["MES"] = df["MES"].round(0).astype("Int64")

    # 🔧 AÑO seguro
    df["AÑO"] = pd.to_numeric(df["AÑO"], errors="coerce").astype("Int64")
    anio_seleccionado = int(anio_seleccionado)
    df = df[df["AÑO"] == anio_seleccionado]

    # 🔧 FILTRO GRUPO (TE FALTABA AQUÍ)
    df = df[df["GRUPO"].isin(companias)]

    # 🔧 IMPORTE CRÍTICO
    df["Importe"] = (
        df["Importe"]
        .astype(str)
        .str.replace("€", "", regex=False)
        .str.replace(",", "", regex=False)
    )

    df["Importe"] = pd.to_numeric(df["Importe"], errors="coerce")
    df = df.dropna(subset=["Importe"])

   



    # 📊 groupby seguro
    df_resultado = (
        df.groupby(["GRUPO", "MES"])["Importe"]
        .sum()
        .reset_index()
    )

    df_pivot = df_resultado.pivot_table(
        index="GRUPO",
        columns="MES",
        values="Importe",
        aggfunc="sum"
    )

    # 🔥 Asegurar meses 1–12
    meses = list(range(1, 13))
    df_pivot = df_pivot.reindex(columns=meses, fill_value=0)

    # 🔥 Rellenar NaN por si acaso
    df_pivot = df_pivot.fillna(0)

    # 🔥 TOTAL por fila (por grupo)
    df_pivot["TOTAL fila"] = df_pivot.sum(axis=1)

    # 🔥 TOTAL por columna (meses)
    df_pivot.loc["TOTAL mes"] = df_pivot.drop(columns=["TOTAL fila"]).sum()

    # recalcular última celda correctamente
    df_pivot.loc["TOTAL mes", "TOTAL fila"] = df_pivot["TOTAL fila"].sum()
    


  

    # 📌 devolver solo los 10 primeros
    return df_pivot






def mostrar_tabla(datos_filtrados, color_fondo="#ccffcc", table_id="tabla_1"):

    # Reset índice
    datos_filtrados = datos_filtrados.reset_index()
    datos_filtrados.columns.name = None

    # HTML de la tabla
    html_table = datos_filtrados.to_html(
        index=False,
        header=True,
        table_id=table_id,
        escape=False,
        float_format="{:,.2f}".format
    )

    # CSS específico para ESTA tabla (no global)
    css = f"""
    <style>
    table#{table_id} {{
        width: auto;
        border-collapse: collapse;
        margin-left: auto;
        margin-right: auto;
    }}

    /* filas */
    table#{table_id} tbody tr {{
        text-align: center;
        padding: 1px;
    }}

    /* cabecera */
    table#{table_id} thead th {{
        background-color: #D9E6E7;
        text-align: center;
        padding: 1px;
    }}

    /* última fila (TOTAL) */
    table#{table_id} tbody tr:last-child {{
        font-weight: bold !important;
    }}

    /* bordes */
    table#{table_id} td {{
        border: 1px solid #ccc;
    }}

    /* Primera columna */
    table#{table_id} td:first-child {{
        text-align: left;
        font-weight: bold;
    }}

    /* Resto de columnas */
    table#{table_id} td:not(:first-child) {{
        text-align: right;
    }}

    /* ANCHOS */
    table#{table_id} th:first-child,
    table#{table_id} td:first-child {{
        width: 160px;
    }}

    table#{table_id} th:last-child,
    table#{table_id} td:last-child {{
        width: 120px;
    }}

    table#{table_id} th:not(:first-child):not(:last-child),
    table#{table_id} td:not(:first-child):not(:last-child) {{
        width: 100px;
    }}

    /* FILAS PARES */
    table#{table_id} tbody tr:nth-child(even) {{
        background-color: {color_fondo} !important;
    }}

    /* FILAS IMPARES */
    table#{table_id} tbody tr:nth-child(odd) {{
        background-color: #ffffff !important;
    }}

    </style>
    """

    # Render
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(html_table, unsafe_allow_html=True)



    #***************************************************************************
    #*********************************************suma listas ******************
    #***************************************************************************

def suma_listas (lista1,lista2):
    
    lista3=[(a if isinstance(a, (int, float)) else 0) +
    (b if isinstance(b, (int, float)) else 0)
    for a, b in zip(lista1, lista2) ]

    return lista3



#*****************************************************************
#**************************************mostrar dos array con titulo
#*****************************************************************
    
def mostrar_dos_arrays_texto(lista1, lista2, texto, table_id="tabla_2lista"):

    import pandas as pd
    import streamlit as st

    # columnas sí a string
    columnas = list(map(str, lista1))

    # ❌ NO convertir lista2 a string
    # lista2 = list(map(str, lista2))

    # fila
    fila = [texto] + lista2

    # ajustar tamaño
    if len(fila) < len(columnas):
        fila += [""] * (len(columnas) - len(fila))
    elif len(fila) > len(columnas):
        fila = fila[:len(columnas)]

    df = pd.DataFrame([fila], columns=columnas)

    # 💡 CLAVE: redondear si hay números
    df = df.map(lambda x: round(x, 2) if isinstance(x, (int, float)) else x)

    html_table = df.to_html(
        index=False,
        header=True,
        table_id=table_id,
        escape=False,
        float_format="{:,.2f}".format
    )

    css = f"""
    <style>
    table#{table_id} {{
        width: auto;
        border-collapse: collapse;
        margin-left: auto;
        margin-right: auto;
    }}

    table#{table_id} thead th {{
        background-color: #D9E6E7;
        text-align: center;
        padding: 2px;
    }}

    table#{table_id} tbody tr {{
        background-color: white;
        text-align: center;
    }}

    table#{table_id} td {{
        border: 1px solid #ccc;
    }}

    table#{table_id} td:first-child {{
        text-align: left;
        font-weight: bold;
        width: 160px;
    }}

    table#{table_id} td:not(:first-child) {{
        text-align: right;
        width: 100px;
    }}

    table#{table_id} td:last-child {{
        width: 120px;
    }}

    table#{table_id} tbody tr:last-child td:last-child {{
        font-weight: bold !important;
    }}
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)
    st.markdown(html_table, unsafe_allow_html=True)



#*****************************************************************
#**************************************obtener lista con los elementos de una columna de pandas
#*****************************************************************


def obtener_columna_lista(df, num_columna):
    """
    Devuelve una lista con los valores de una columna,
    ignorando la primera fila (cabecera real de datos).
    """

    return (
        df.iloc[0:, num_columna]   # 🔥 saltamos la primera fila
        .dropna()                 # quitamos NaN
        .astype(str)              # convertimos a texto
        .tolist()                 # lista final
    )



#*****************************************************************
#**************************************patrones año
#*****************************************************************

def busca_patrones_año(df_datos, anio_seleccionado):

    df = df_datos.copy()

    # 🔧 asegurar tipo numérico en AÑO
    df["AÑO"] = pd.to_numeric(df["AÑO"], errors="coerce")

    # 📅 filtrar por año
    df = df[df["AÑO"] == anio_seleccionado]

    # 🧠 obtener valores únicos de GRUPO
    lista_grupos = df["GRUPO"].dropna().unique().tolist()



    return lista_grupos



#*****************************************************************
#************************************** Recopila patrones
#*****************************************************************

def recopila_patrones(df_patrones):

    # 🔧 convertir todo a una sola serie
    serie = df_patrones.stack()

    # 🧹 eliminar vacíos y NaN
    serie = serie.dropna()


    # 🔤 convertir a lista
    return serie.astype(str).tolist()


#*****************************************************************
#************************************** Elementos no incluidos
#*****************************************************************


def elementos_no_incluidos(lista1, lista2):
    """
    Devuelve los elementos de lista1 que NO están en lista2.
    """

    set2 = set(lista2)

    return [x for x in lista1 if x not in set2]


#*****************************************************************
#************************************** Filtro por año
#*****************************************************************



def tabla_filtro_año(df_datos, companias, lista_anios):

    df = df_datos.copy()

    # 🔧 limpiar columnas clave
    df["AÑO"] = pd.to_numeric(df["AÑO"], errors="coerce")
    df["Importe"] = pd.to_numeric(df["Importe"], errors="coerce")

    # 🧹 eliminar filas malas
    df = df.dropna(subset=["AÑO", "Importe"])

    df["AÑO"] = df["AÑO"].astype(int)

    # 🔧 filtrar compañías
    df = df[df["GRUPO"].isin(companias)]

    # 📊 pivot seguro
    df_resultado = df.pivot_table(
        index="GRUPO",
        columns="AÑO",
        values="Importe",
        aggfunc="sum"
    )

    # 🚀 forzar años
    df_resultado = df_resultado.reindex(columns=lista_anios, fill_value=0)

    df_resultado = df_resultado.fillna(0)

    # 🔥 totales
    df_resultado["TOTAL"] = df_resultado.sum(axis=1)
    df_resultado.loc["TOTAL"] = df_resultado.drop(columns=["TOTAL"]).sum()
    df_resultado.loc["TOTAL", "TOTAL"] = df_resultado["TOTAL"].sum()

    return df_resultado




#*****************************************************************
#**************************************patrones año total
#*****************************************************************

def busca_patrones_total(df_datos, lista_años):

    df = df_datos.copy()

    lista_grupos=[]
    for año in lista_años:
          patrones_años= busca_patrones_año(df_datos, año)  
          lista_grupos.append(patrones_años)  


  

    return lista_grupos


#*****************************************************************
#**************************************suma valores positivos
#*****************************************************************


def suma_positivos_por_anio(df, lista_anios, lista_grupos):

    df = df.copy()

    # 🔧 CLAVE: convertir a número
    df["Importe"] = pd.to_numeric(df["Importe"], errors="coerce")

    # 🔧 eliminar valores no válidos
    df = df.dropna(subset=["Importe"])

    resultado = []

    for año in lista_anios:
        suma = df.loc[
            (df["AÑO"] == año) &
            (df["Importe"] > 0) &
            (df["GRUPO"].isin(lista_grupos)),
            "Importe"
        ].sum()

        resultado.append(suma)

    return resultado

#*****************************************************************
#**************************************suma valores negativos
#*****************************************************************


def suma_negativos_por_anio(df, lista_anios, lista_grupos):

    df = df.copy()

    # 🔧 convertir a numérico
    df["Importe"] = pd.to_numeric(df["Importe"], errors="coerce")

    # 🔧 eliminar valores inválidos
    df = df.dropna(subset=["Importe"])

    resultado = []

    for año in lista_anios:
        suma = df.loc[
            (df["AÑO"] == año) &
            (df["Importe"] < 0) &
            (df["GRUPO"].isin(lista_grupos)),
            "Importe"
        ].sum()

        resultado.append(suma)

    return resultado


#*****************************************************************
#**************************************suma valores positivos por meses
#*****************************************************************

def suma_positivos_por_anio_mes(df, lista_anios, lista_meses, lista_grupos):

    df = df.copy()

    # 🔧 convertir tipos críticos
    df["Importe"] = pd.to_numeric(df["Importe"], errors="coerce")
    df["AÑO"] = pd.to_numeric(df["AÑO"], errors="coerce")
    df["MES"] = pd.to_numeric(df["MES"], errors="coerce")

    # 🔧 eliminar filas inválidas
    df = df.dropna(subset=["Importe", "AÑO", "MES"])

    df["AÑO"] = df["AÑO"].astype(int)
    df["MES"] = df["MES"].astype(int)

    # 🔹 filtrar
    df_filtrado = df[
        (df["AÑO"].isin(lista_anios)) &
        (df["MES"].isin(lista_meses)) &
        (df["GRUPO"].isin(lista_grupos)) &
        (df["Importe"] > 0)
    ]

    # 🔹 agrupar
    agrupado = df_filtrado.groupby(["AÑO", "MES"])["Importe"].sum()

    valores = []
    etiquetas = []

    # 🔹 generar listas alineadas
    for año in sorted(lista_anios):
        for mes in sorted(lista_meses):

            valores.append(agrupado.get((año, mes), 0))
            etiquetas.append(f"{año}-{mes:02d}")

    return valores, etiquetas


#*****************************************************************
#**************************************suma valores positivos por meses agrupado por mes
#*****************************************************************






def suma_positivos_por_anio_mes2(df, lista_anios, lista_meses, lista_grupos):

    df = df.copy()

    # 🔧 convertir tipos (CLAVE)
    df["Importe"] = pd.to_numeric(df["Importe"], errors="coerce")
    df["AÑO"] = pd.to_numeric(df["AÑO"], errors="coerce")
    df["MES"] = pd.to_numeric(df["MES"], errors="coerce")

    # 🔧 eliminar valores inválidos
    df = df.dropna(subset=["Importe", "AÑO", "MES"])

    df["AÑO"] = df["AÑO"].astype(int)
    df["MES"] = df["MES"].astype(int)

    # 🔹 filtrar datos
    df_filtrado = df[
        (df["AÑO"].isin(lista_anios)) &
        (df["MES"].isin(lista_meses)) &
        (df["GRUPO"].isin(lista_grupos)) &
        (df["Importe"] > 0)
    ]

    # 🔹 agrupar (MES, AÑO)
    agrupado = df_filtrado.groupby(["MES", "AÑO"])["Importe"].sum()

    valores = []
    etiquetas = []

    # 🔹 orden: meses → años
    for mes in sorted(lista_meses):
        for año in sorted(lista_anios):

            valores.append(agrupado.get((mes, año), 0))
            etiquetas.append(f"{mes:02d}-{año}")

    return valores, etiquetas


#*****************************************************************
#**************************************suma valores positivos por meses
#*****************************************************************


def suma_negativos_por_anio_mes(df, lista_anios, lista_meses, lista_grupos):

    df = df.copy()

    # 🔧 convertir tipos (CLAVE)
    df["Importe"] = pd.to_numeric(df["Importe"], errors="coerce")
    df["AÑO"] = pd.to_numeric(df["AÑO"], errors="coerce")
    df["MES"] = pd.to_numeric(df["MES"], errors="coerce")

    # 🔧 limpiar nulos
    df = df.dropna(subset=["Importe", "AÑO", "MES"])

    df["AÑO"] = df["AÑO"].astype(int)
    df["MES"] = df["MES"].astype(int)

    # 🔹 filtrar
    df_filtrado = df[
        (df["AÑO"].isin(lista_anios)) &
        (df["MES"].isin(lista_meses)) &
        (df["GRUPO"].isin(lista_grupos)) &
        (df["Importe"] < 0)
    ]

    # 🔹 agrupar
    agrupado = df_filtrado.groupby(["AÑO", "MES"])["Importe"].sum()

    valores = []
    etiquetas = []

    # 🔹 generar listas alineadas
    for año in sorted(lista_anios):
        for mes in sorted(lista_meses):

            valores.append(agrupado.get((año, mes), 0))
            etiquetas.append(f"{año}-{mes:02d}")

    return valores, etiquetas



#*****************************************************************
#**************************************suma valores positivos por meses agrupado por mes
#*****************************************************************






def suma_negativos_por_anio_mes2(df, lista_anios, lista_meses, lista_grupos):

    df = df.copy()

    # 🔧 limpieza obligatoria
    df["Importe"] = pd.to_numeric(df["Importe"], errors="coerce")
    df["AÑO"] = pd.to_numeric(df["AÑO"], errors="coerce")
    df["MES"] = pd.to_numeric(df["MES"], errors="coerce")

    df = df.dropna(subset=["Importe", "AÑO", "MES"])

    df["AÑO"] = df["AÑO"].astype(int)
    df["MES"] = df["MES"].astype(int)

    # 🔹 filtrar datos
    df_filtrado = df[
        (df["AÑO"].isin(lista_anios)) &
        (df["MES"].isin(lista_meses)) &
        (df["GRUPO"].isin(lista_grupos)) &
        (df["Importe"] < 0)
    ]

    # 🔹 agrupar MES-AÑO
    agrupado = df_filtrado.groupby(["MES", "AÑO"])["Importe"].sum()

    valores = []
    etiquetas = []

    for mes in sorted(lista_meses):
        for año in sorted(lista_anios):
            valores.append(agrupado.get((mes, año), 0))
            etiquetas.append(f"{mes:02d}-{año}")

    return valores, etiquetas


#*****************************************************************
#**************************************suma valores positivos por años
#*****************************************************************


def suma_positivos_por_año_grupo(df, lista_anios, lista_grupos):

    df = df.copy()

    # 🔧 convertir a numérico (CLAVE)
    df["Importe"] = pd.to_numeric(df["Importe"], errors="coerce")
    df["AÑO"] = pd.to_numeric(df["AÑO"], errors="coerce")

    # 🔧 eliminar valores inválidos
    df = df.dropna(subset=["Importe", "AÑO"])

    df["AÑO"] = df["AÑO"].astype(int)

    resultado = []

    for año in lista_anios:
        suma = df.loc[
            (df["AÑO"] == año) &
            (df["Importe"] > 0) &
            (df["GRUPO"].isin(lista_grupos)),
            "Importe"
        ].sum()

        resultado.append(suma)

    return resultado



#*****************************************************************
#**************************************suma valores positivos por años
#*****************************************************************


def suma_negativos_por_año_grupo(df, lista_anios, lista_grupos):

    df = df.copy()

    # 🔧 convertir a numérico (OBLIGATORIO)
    df["Importe"] = pd.to_numeric(df["Importe"], errors="coerce")
    df["AÑO"] = pd.to_numeric(df["AÑO"], errors="coerce")

    # 🔧 limpiar valores inválidos
    df = df.dropna(subset=["Importe", "AÑO"])

    df["AÑO"] = df["AÑO"].astype(int)

    resultado = []

    for año in lista_anios:
        suma = df.loc[
            (df["AÑO"] == año) &
            (df["Importe"] < 0) &
            (df["GRUPO"].isin(lista_grupos)),
            "Importe"
        ].sum()

        resultado.append(suma)

    return resultado
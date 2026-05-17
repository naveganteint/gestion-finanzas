import streamlit as st

from styles.estilos import aplicar_estilos
st.set_page_config(
    page_title="Gestor Financiero",
    page_icon="🧮",
    #page_icon="assets/calculadora.png"
    layout="wide"
)

aplicar_estilos()

st.markdown(
    """
    <h1 style='text-align:center; color:#2E3A59 ;'>
     <i class="bi bi-calculator" style="color: currentColor;">&nbsp;&nbsp; Gestor Financiero</i>
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h3 style='text-align:center; color:#2E3A59 ;'>
       <i class="bi bi-graph-up" style="color: currentColor;"</i>&nbsp;&nbsp; Control de ingresos y gastos de empresa</i>
    </h3>
    """,
    unsafe_allow_html=True
)

#st.image("assets/logo.png", width=200)





# Inicializar session_state global
if "hojas" not in st.session_state:
    st.session_state.hojas = {}





#st.markdown('<h1 style="text-align: center;color: #2E3A59 ;">Quick Stock View </h1>', unsafe_allow_html=True)



st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css" rel="stylesheet">

<div style="text-align:center; font-size:200px; color: #2E3A59 ;">
    <i class="bi bi-search" style="color: currentColor;"></i>
</div>
""", unsafe_allow_html=True)


st.write("")
st.write("")

st.markdown(
    """
    <div style="
        background-color: white;
        color: #2E3A59 ;
        padding: 15px;
        font-size: 20px;
        text-align: center;
    ">
        Pagina inicial de la aplicacion de Gestion de finanzas
    </div>
    """,
    unsafe_allow_html=True
)

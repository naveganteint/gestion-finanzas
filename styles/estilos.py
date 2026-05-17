
import streamlit as st

#2E3A59 (azul grisáceo elegante)

#complementario F2C6C2 (rosa palo / maquillaje)





def aplicar_estilos():
    st.markdown(
        """
        <style>

        /* Fondo sidebar */
        [data-testid="stSidebar"] {
            background-color: white;
        }

        /* Hacer que cada enlace ocupe toda la línea */
        [data-testid="stSidebarNav"] a {
            display: block;
            width: 100%;
            padding: 10px 12px;
            border-radius: 8px;
            transition: all 0.3s ease;
            background-color: #C2DAC1  /* color de fondo constante */
        }

        /* Texto del menú */
        [data-testid="stSidebarNav"] span {
            color: #2E3A59 !important;
            font-weight: bold;
            font-size: 18px;
            
        }

        /* Hover en TODA la línea */
        [data-testid="stSidebarNav"] a:hover {
            background-color: #F2C6C2 !important;
        }

        /* Cambiar color del texto en hover */
        [data-testid="stSidebarNav"] a:hover span {
            color: black !important;
        }

        /* Página seleccionada (activa) */
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background-color: #8AA1C1 !important;
        }




        </style>
        """,
        unsafe_allow_html=True

    )




def h3_especial(texto, color_fondo="#C2DAC1"): 
    """
    Muestra un título h3 centrado, con texto color #1b3865
    y fondo de la mitad de la pantalla color #DABBED.
    """
    st.markdown(f"""
    <div style="
        width: 70%;                /* ancho del div */
        background-color:  {color_fondo};
        text-align: center;
        padding: 2px 0;            /* padding vertical mínimo */
        margin: 0 auto;             /* centra horizontalmente */
        border-radius: 4px;
    ">
        <span style="
            color: #1b3865;
            font-size: 24px;
            font-weight: bold;
        ">{texto}</span>
    </div>
    """, unsafe_allow_html=True)



#************************************************ texto separador ***********************


def h2_especial(texto, color_fondo="#C2DAC1"):
    """
    Título h2 estilizado con color de fondo configurable.
    """

    st.markdown(f"""
    <div style="
        width: 30%;
        background-color: {color_fondo};
        text-align: left;
        padding: 2px 25px;
        margin: 0 200px;
        border-radius: 4px;
    ">
        <span style="
            color: #1b3865;
            font-size: 16px;
            font-weight: bold;
        ">{texto}</span>
    </div>
    """, unsafe_allow_html=True)

# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 09:22:15 2023

@author: above
"""

import streamlit as st
import pandas as pd
import extractor_pyairtable as ext_pyat
from datetime import datetime
import time
from streamlit_autorefresh import st_autorefresh
import os
import pantalla_jugador as p_jugador
import callbacks
import pantalla_creador as p_creador
import base64

#import plotly.express as px
#from PIL import Image
#import os
#from millify import millify



# mandangues de la pàgina -------------------------------------------------
st.set_page_config(
    page_title="Joc de la sostenibilitat",
    layout="wide",
    
)


# ---------------- IMATGE FONS DE PANTALLA ---------------- #
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = """
    <style>
        [data-testid="stAppViewContainer"]{
            background-image: url("data:image/png;base64,%s");
            background-size: cover;
            background-position-x: right 250px;
            background-position-y: bottom 0px;
        }
        [data-testid="stHeader"]{
            background-color: rgba(0,0,0,0); /*Header transparent*/
        }
    </style>

    """ % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('./assets/img/mountains.jpg')

# ---------------- INICI ESTILS DE LA PÀGINA MAIN ---------------- #

#st.write(st.session_state)
##Paràmetres i variables d'inici ---------------------------------------------------------------
if 'token' not in st.session_state:
    st.session_state.token = st.secrets['token_joc_sostenibilitat']
    st.session_state.id_t_Registre_partides = st.secrets['id_t_Registre_partides']
    st.session_state.id_t_Historic_partides = st.secrets['id_t_Historic_partides']
    st.session_state.id_t_Aliments = st.secrets['id_t_Aliments']
    st.session_state.id_t_Productes_habitatge = st.secrets['id_t_Productes_habitatge']
    st.session_state.id_t_Productes_transport = st.secrets['id_t_Productes_transport']
    st.session_state.id_t_Oci = st.secrets['id_t_Oci']
    st.session_state.id_t_Esdeveniments = st.secrets['id_t_Esdeveniments']
    st.session_state.id_t_Possessions = st.secrets['id_t_Possessions']
    st.session_state.id_base = st.secrets['id_base_joc_sostenibilitat']

if 'creacio' not in st.session_state:
    try:
        st.session_state.pantalla_inici = st.query_params['pantalla_inici']
        #https://your_app.streamlit.app/?pantalla_inici=creador
    except:
        st.session_state.pantalla_inici = 'jugador'



if st.session_state.pantalla_inici == 'creador':
    # pantalla per creador abans d'entrar a la partida o de crear-la
    if 'acces_admin' not in st.session_state:
        p_creador.entra_crea()
    #pantalla creador al entrar a la partida
    elif st.session_state.estat_partida == 'Per iniciar' and st.session_state.acces_admin == True:
        p_creador.iniciar()
    #pantalla creador d'una partida iniciada
    elif st.session_state.estat_partida == 'En joc' and st.session_state.acces_admin == True:
        p_creador.partida()
    elif st.session_state.estat_partida == 'Finalitzada' and st.session_state.acces_admin == True:
        p_creador.fi_partida()

    

if st.session_state.pantalla_inici == 'jugador':   
    #pantalla abans d'entrar a la partida el jugador
    if 'ingres_partida' not in st.session_state:
        p_jugador.entra_crea()
        
    #Pantalla després d'entrar a la partida el jugador però partida encara pendent d'iniciar-se
    elif st.session_state.estat_partida == 'Per iniciar' and st.session_state.ingres_partida == True:
        p_jugador.iniciar()
        
    #Pantalla al iniciar-se la partida pel jugador   
    elif st.session_state.estat_partida == 'En joc' and st.session_state.ingres_partida == True:
        p_jugador.partida()
        
    #Pantalla al acabar-se la partida
    elif st.session_state.estat_partida == 'Finalitzada' and st.session_state.ingres_partida == True:
        p_jugador.fi_partida()

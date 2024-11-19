# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 20:47:33 2024

@author: adria
"""
import streamlit as st
import callbacks
import time
from streamlit_autorefresh import st_autorefresh
import alertes_modals as modals
from modal_inicial import modal_inicial_events
from login2 import login_events2
from login import login_events
from sidebar import sidebar_events 
from modal_products import modal_products_events 
from modal_economia import modal_economia_events
import json

def entra_crea():
    # m = modal_economia_events()
    # Funció que crida el contenidor del login i retorna els valors dels inputs en un json
    value = login_events2()

    if value:
        st.markdown("""
            <style>
                [title="login2.login2"]{
                    display: none;
                }
                    </style>
                    """, unsafe_allow_html=True)
        modals.modal_carregant()
        st.session_state.nom_partida = value["nom_partida"]
        st.session_state.nom_jugador = value["nom_jugador"]
        st.session_state.contrassenya = value["codi"]

        callbacks.acces_callback()

        if "id_partida" in st.session_state:
            st.rerun()


def iniciar():
    modals.modal_carregant_el_joc()
    
    # Refresquem automaticament cada 5 segons
    count = st_autorefresh(interval=5 * 1000, limit=2000, key="fizzbuzzcounter")
    callbacks.estat_partida_callback()
    
def partida():
    clicked = modal_inicial_events()
    if clicked == "True":
        st.session_state.ronda_actual = st.session_state.historic_jugador['Ronda'].max()
        callbacks.actualitzar_historic_partida()
        dictJugador = {
            "Nom_jugador": st.session_state.nom_jugador,
            "Nom_partida": st.session_state.nom_partida,
            "Salari": round(st.session_state.historic_jugador['Salari'].loc[len(st.session_state.historic_jugador)-1],2),
            "Necessitats_transport": st.session_state.historic_jugador['Necessitats_transport'].loc[len(st.session_state.historic_jugador)-1],
            "Necessitats_habitatge": st.session_state.historic_jugador['Necessitats_habitatge'].loc[len(st.session_state.historic_jugador)-1],
            "EconomiaTotal": st.session_state.historic_jugador['Economia'].loc[len(st.session_state.historic_jugador)-1],
            "Salut": st.session_state.historic_jugador['Salut'].tolist(),
            "Economia": st.session_state.historic_jugador['Economia'].tolist(),
            "Ronda": st.session_state.historic_jugador['Ronda'].tolist(),
            "Nivell": st.session_state.historic_jugador['Nivell'].loc[len(st.session_state.historic_jugador)-1],
            "Ronda_actual": st.session_state.ronda_actual,
            "Aliments": st.session_state.historic_jugador['Aliments'].loc[len(st.session_state.historic_jugador)-1],
            "Temps": st.session_state.historic_jugador['Temps'].loc[len(st.session_state.historic_jugador)-1],
            "Despesa": st.session_state.historic_jugador['Energia'].loc[len(st.session_state.historic_jugador)-1] * st.session_state.f_energia_cost
        }
        
        stringDictAliments = st.session_state.aliments
        stringDictHabitatge = st.session_state.productes_habitatge
        stringDictTransport = st.session_state.productes_transport
        stringDictOci = st.session_state.oci
        
        if "possessions_habitatge_restringides" not in st.session_state or "possessions_transport_restringides" not in st.session_state or "possessions_transport" not in st.session_state:
            callbacks.actualitzar_possessions_restringides()
        stringDictHabitatgeBloc = st.session_state.possessions_habitatge_restringides
        stringDictTransportOwn = st.session_state.possessions_transport_restringides
        stringDictHabitatgeOwn = st.session_state.possessions_habitatge
        
        #st.write(dictJugador)

        # Transformem el diccionari creat amb la informació del jugador a tipus String per poder enviar-ho al javascript
        stringDictJugador = "{" + ", ".join([f'"{clave}": "{valor}"' for clave, valor in dictJugador.items()]) + "}"
        
        # Traiem el padding del contenidor principal abans de crear el dashboard
        st.markdown("""
            <style>
                [data-testid="block-container"].st-emotion-cache-z5fcl4{
                    padding: 0rem 2rem 2rem 2rem!important;
                }
                [title="modal_inicial.modal_inicial"]{
                    display: none;
                }
                    </style>
                    """, unsafe_allow_html=True)
        
        if "var_nova_ronda" not in st.session_state:
            st.session_state.var_nova_ronda = False
            print("Acabem d'inicialitzar la variable de nou")
            print(st.session_state.var_nova_ronda)
            
        
        print('Estem en una ronda no nova')
        print(st.session_state.var_nova_ronda)
        # Cridem el dashboard
        if st.session_state.historic_partida.loc[:,'Ronda'].max() != st.session_state.ronda_actual:
            with st.spinner('Esperant a que tothom finalitzi la ronda'):
                print('Estem esperant els altres jugadors')
                print(st.session_state.var_nova_ronda)
                time.sleep(5)
                st.rerun()
        else:
            
            if "var_nova_ronda" in st.session_state:
                if st.session_state.var_nova_ronda == True:
                    economia_events_clicked = modal_economia_events(stringDictJugador)
                    if economia_events_clicked == "True":
                        st.session_state.var_nova_ronda = False
                        print('Estem a linici duna nova ronda')
                        print(st.session_state.var_nova_ronda)
                        economia_events_clicked = "False"
                        st.rerun()
                
            compres = sidebar_events(stringDictJugador,stringDictAliments, stringDictHabitatge, stringDictOci, stringDictTransport, stringDictHabitatgeBloc, stringDictHabitatgeOwn, stringDictTransportOwn)
            if compres is not None and compres !=[]:
                callbacks.guardar_accio_callback(compres)
                st.rerun()

            passar_ronda = st.button('Següent ronda!')
            if passar_ronda:
                callbacks.passar_ronda_jugador()
                st.session_state.var_nova_ronda = True
                print('Estem just després dapretar el botó')
                print(st.session_state.var_nova_ronda)
                st.rerun()
                     
    
def fi_partida():
    st.write('Final partida')
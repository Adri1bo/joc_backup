# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 15:25:25 2024

@author: adria
"""

import streamlit as st
import extractor_pyairtable as ext_pyat
from datetime import datetime
import time
import pandas as pd
import numpy as np
from scipy.stats import norm
from streamlit_autorefresh import st_autorefresh


##Funcions de callbacks ---------------------------------------------------------------

# %%Funcions tractament dades generals
def descomprimir_field(df,nom_compressed_field):
    df = df.reset_index(drop=True)
    df_resultat_final=pd.DataFrame()
    for i in range(len(df)):
        df_descomprimit = ext_pyat.split_json_to_df(df[nom_compressed_field][i])
        nou_df = df.drop(nom_compressed_field, axis=1).loc[[i]]
        nou_df_repetit = nou_df.loc[nou_df.index.repeat(len(df_descomprimit))].reset_index(drop=True)
        resultat = pd.concat([df_descomprimit, nou_df_repetit], axis=1)
        df_resultat_final = pd.concat([df_resultat_final, resultat], axis=0)
    return df_resultat_final

def formatejar_df_jugadors(df_jugadors):
    df = df_jugadors
    df['Salari'] = df_jugadors['Salari'].apply(lambda x: "{:.2f}€".format((x)))
    df['Economia'] = df_jugadors['Economia'].apply(lambda x: "{:.2f}€".format((x)))
    df['Salut'] = df_jugadors['Salut'].apply(lambda x: round(x,0))
    df['Necessitats_transport'] = df_jugadors['Necessitats_transport'].apply(lambda x: "{:.0f}%".format(x))
    df['Necessitats_habitatge'] = df_jugadors['Necessitats_habitatge'].apply(lambda x: "{:.0f}%".format(x))
    
    return df



# %% Retrieve dades
def cuina_possessions_habitatge(possessions_habitatge):
    # Primer si a possessions habitatge no hi ha res només podran comprar el disseny
    print(possessions_habitatge)
    if possessions_habitatge.empty:
        productes_no_escollibles = st.session_state.productes_habitatge_df[st.session_state.productes_habitatge_df['tipologia_producte'] != '1']['Nom'].tolist()
        print(productes_no_escollibles)
    # Segon si ja han comprat el disseny, si aquest és el convencional no podran escollir els extres ni els que la tipologia coincideixei
    elif (possessions_habitatge['Nom'] == 'Disseny i arquitectura convencional').any():
        print('Hem entrat al convencional')
        productes_no_escollibles = st.session_state.productes_habitatge_df[st.session_state.productes_habitatge_df['tipologia_producte'].str.contains('Extra')]['Nom'].tolist()
        productes_no_escollibles.extend(st.session_state.productes_habitatge_df[st.session_state.productes_habitatge_df['tipologia_producte'].isin(possessions_habitatge['tipologia_producte'])]['Nom'].tolist())
        print(productes_no_escollibles) 
        productes_no_escollibles=list(set(productes_no_escollibles))
    # Segon si ja han comprat el disseny, si aquest és el sostenible no podran escollir els extres ni els que la tipologia coincideixei
    elif (possessions_habitatge['Nom'] == 'Disseny i arquitectura sostenible').any():
        print(possessions_habitatge)
        productes_no_escollibles = st.session_state.productes_habitatge_df[st.session_state.productes_habitatge_df['tipologia_producte'].isin(possessions_habitatge['tipologia_producte'])]['Nom'].tolist()
        
    #treiem del productes no escollibles els que són ja posseits
    try:
        noms_possessions=set(possessions_habitatge['Nom'])
    except:
        noms_possessions=set()
    
    productes_no_escollibles = list(set(productes_no_escollibles)-noms_possessions)
        
    return productes_no_escollibles

def actualitzar_possessions_restringides():
    record = ext_pyat.obtenir_record(st.session_state.token,
                            st.session_state.id_base,
                            st.session_state.id_t_Possessions,
                            columna=['Id_jugador'],
                            coincidencia=[st.session_state.id_jugador])
    st.session_state.possessions_jugador = ext_pyat.obtenir_field_of_record(record[0],
                                                                         camp = 'dades',
                                                                         string_2_df = True)
    print(st.session_state.possessions_jugador)
    try:
        possessions_habitatge = st.session_state.possessions_jugador[st.session_state.possessions_jugador["Tipus"] == 'Habitatge']
        print(possessions_habitatge)
        st.session_state.possessions_habitatge = list(possessions_habitatge['Nom'])
    except:
        print("Ha saltat l'excepció")
        possessions_habitatge = pd.DataFrame()
        st.session_state.possessions_habitatge = []
        
    st.session_state.possessions_habitatge_restringides = cuina_possessions_habitatge(possessions_habitatge)
    
    
    try:
        st.session_state.possessions_transport_restringides = st.session_state.possessions_jugador[st.session_state.possessions_jugador["Tipus"] == 'Transport']['Nom'].tolist()
    except:
        st.session_state.possessions_transport_restringides = []

def actualitzar_historic_jugador():
    record = ext_pyat.obtenir_record_per_id(st.session_state.token,
                                   st.session_state.id_base,
                                   st.session_state.id_t_Historic_partides,
                                   st.session_state.id_jugador)
    st.session_state.historic_jugador = ext_pyat.obtenir_field_of_record(record,
                                                                         camp = 'dades',
                                                                         string_2_df = True)

def actualitzar_historic_partida():
    record = ext_pyat.obtenir_record_per_id(st.session_state.token,
                                   st.session_state.id_base,
                                   st.session_state.id_t_Registre_partides,
                                   st.session_state.id_partida)
    
    st.session_state.historic_partida = ext_pyat.obtenir_field_of_record(record,
                                                                         camp = 'dades',
                                                                         string_2_df = True)


def df_jugadors_callback():
    df_jugadors, table_jugadors = ext_pyat.obtenir_taula(st.session_state.token,
                                      st.session_state.id_base,
                                      st.session_state.id_t_Historic_partides,
                                      columna_filtre='Id_partida',
                                      v_columna_filtre=st.session_state.id_partida)
    st.session_state.df_jugadors = descomprimir_field(df_jugadors,'dades')


def estat_partida_callback():
    record = ext_pyat.obtenir_record_per_id(st.session_state.token,
                                            st.session_state.id_base,
                                            st.session_state.id_t_Registre_partides,
                                            st.session_state.id_partida)
    st.session_state.estat_partida = ext_pyat.obtenir_field_of_record(record,'Estat')
    

# %% funcions de crear partida i accedir a la partida
    
def iniciar_partida_callback():
    #Obtenim les dades de tots els jugadors
    df_jugadors_callback()
    st.session_state.ronda_actual = 1
    #modifiquem el df per què només tingui la última ronda
    df_util = st.session_state.df_jugadors[st.session_state.df_jugadors['Ronda']==st.session_state.ronda_actual]
    #actualitzem les de la partida per la ronda 1
    actualitzar_historic_partida()
    
    paquet_dades = pd.DataFrame([{
                                "Ronda": st.session_state.ronda_actual,
                                "Nombre de jugadors": df_util.nunique()["id"],
                                "Economia": df_util["Economia"].sum(),
                                "Contaminació": 1000,
                                "Salut": df_util["Salut"].mean(),
                                "Necessitats_transport": df_util["Necessitats_transport"].mean(),
                                "Necessitats_habitatge": df_util["Necessitats_habitatge"].mean(),
                                "Energia":df_util["Energia"].sum(),
                                "Temps":df_util["Temps"].sum(),
                                "Aliments":df_util["Aliments"].sum(),
                                "Salari":df_util["Salari"].mean(),
                                "PIB":df_util["Salari"].sum(),
                                "Nivell_individual":df_util["Nivell"].mean(),
                                "Recursos naturals": 100000,
                                "Recursos energètics": 100000,
                                "Nivell econòmic": 0,
                                "Nivell social": 0,
                                "Nivell mediambiental": -1}])
    paquet_dades = pd.concat([st.session_state.historic_partida,paquet_dades])
    
    dades={"Estat": "En joc",
           "dades": paquet_dades.to_json(orient='split',force_ascii=False)}
    ext_pyat.actualitzar_field_of_record(st.session_state.token,
                                         st.session_state.id_base,
                                         st.session_state.id_t_Registre_partides,
                                         st.session_state.id_partida,
                                         dades)
    st.session_state.estat_partida='En joc'

def sortir_partida_callback():
    for key in st.session_state.keys():
        del st.session_state[key]
    
def acces_admin_callback():
    
    st.session_state.acces_admin = True
    carregar_factors_conversio()
    estat_partida_callback()

def acces_callback():
    if st.session_state.nom_partida != "" and st.session_state.nom_jugador != ""  and st.session_state.contrassenya != ""  :
        #primer obtenim l'identificador de la taula de registre partides
        try:
            st.session_state.id_partida = ext_pyat.obtenir_id_record(st.session_state.token,
                                                                     st.session_state.id_base,
                                                                     st.session_state.id_t_Registre_partides,
                                                                     columna = 'Nom',
                                                                     coincidencia=st.session_state.nom_partida)
            estat_partida_callback()
            
            #guardem les taules d'aliments, productes i oci com a variable al sesion state i au
            df_aliments, taula = ext_pyat.obtenir_taula(st.session_state.token, st.session_state.id_base, st.session_state.id_t_Aliments)
            st.session_state.aliments = df_aliments.to_dict(orient='records')
            
            df_productes_habitatge, taula = ext_pyat.obtenir_taula(st.session_state.token, st.session_state.id_base, st.session_state.id_t_Productes_habitatge)
            st.session_state.productes_habitatge_df = df_productes_habitatge
            st.session_state.productes_habitatge = df_productes_habitatge.to_dict(orient='records')
            
            df_productes_transport, taula = ext_pyat.obtenir_taula(st.session_state.token, st.session_state.id_base, st.session_state.id_t_Productes_transport)
            st.session_state.productes_transport_df = df_productes_transport
            st.session_state.productes_transport = df_productes_transport.to_dict(orient='records')
            
            df_oci, taula = ext_pyat.obtenir_taula(st.session_state.token, st.session_state.id_base, st.session_state.id_t_Oci)
            st.session_state.oci = df_oci.to_dict(orient='records')
            
            carregar_factors_conversio()
            
        except:
            #s'hauria d'aconseguir que s'acabés la funció i et tornés a donar l'opció de posar una partida correcta
            st.error("No s'ha trobat la partida, corregeix el nom")
            time.sleep(2)
        
        if 'id_partida' in st.session_state:
            acces_function()
            
    else:
        st.warning("S'han d'omplir els tres camps")
        time.sleep(2)
           
def acces_function():
    #Obtenim el record del jugador
    record = ext_pyat.obtenir_record(st.session_state.token,
                                     st.session_state.id_base,
                                     st.session_state.id_t_Historic_partides,
                                     columna = ['Id_partida','nom jugador','codi secret'],
                                     coincidencia=[st.session_state.id_partida,st.session_state.nom_jugador,st.session_state.contrassenya])
    
    #Si el jugador no està registrat en la partida retornarà una llista buida, en aquest cas s'hauria de crear el record del jugador 
    #sempre i quan la partida no estigui iniciada
    if record == [] and st.session_state.estat_partida == 'Per iniciar':
        #Calculem els valors inicials pel jugador
        Salari, Economia, Salut, Necessitats_transport, Necessitats_habitatge = inicialitzar_estatus_jugador()
        #Farem un update del camp
        paquet_dades = pd.DataFrame([{
                "Ronda": 1,
                "Contaminació": 0,
                "Aliments": 1,
                "Temps": 2,
                "Energia": 50,
                "Recursos energètics": 0,
                "Recursos naturals": 0,
                "Economia": Economia,
                "Salari": Salari,
                "Salut": Salut,
                "Necessitats_transport": Necessitats_transport,
                "Necessitats_habitatge": Necessitats_habitatge,
                "Nivell": 0}])

        dades={
         'Id_partida':st.session_state.id_partida,
         'nom partida':st.session_state.nom_partida,
         'nom jugador':st.session_state.nom_jugador,
         'codi secret':st.session_state.contrassenya,
         'dades': paquet_dades.to_json(orient='split',force_ascii=False)
         }
        #tercer cal registrar el jugador a la taula vigilant els duplicats de nom
        #Utilitzem una funció específica per una taula comprimida
        status = ext_pyat.afegir_linia(st.session_state.token,
                                        st.session_state.id_base,
                                        st.session_state.id_t_Historic_partides,
                                        dades,
                                        columna_duplicats='nom jugador',
                                        columna_filtre = 'Id_partida',
                                        v_columna_filtre = st.session_state.id_partida)
        
        #inicialitzem la variable que marca inici de ronda
        st.session_state.var_nova_ronda = True
        print("Acabem d'inicialitzar la variable")
        print(st.session_state.var_nova_ronda)
        
        if status == True:
            st.session_state.id_jugador=ext_pyat.obtenir_id_record(st.session_state.token,
                                                                   st.session_state.id_base,
                                                                   st.session_state.id_t_Historic_partides,
                                                                   columna = ['nom jugador','Id_partida','codi secret'],
                                                                   coincidencia=[st.session_state.nom_jugador,st.session_state.id_partida,st.session_state.contrassenya])

            
        
        else:
            st.error("Nom de jugador ja escollit o contrassenya incorrecta, modifica'l siusplau")
            time.sleep(2)
        
        #Utilitzem inicialitzem també la línia de possessions
        paquet_dades = pd.DataFrame([{'Ronda':0}])
        
        dades={
         'Id_jugador':st.session_state.id_jugador,
         'Id_partida':st.session_state.id_partida,
         'Nom jugador':st.session_state.nom_jugador,
         'Nom partida':st.session_state.nom_partida,
         'dades': paquet_dades.to_json(orient='split',force_ascii=False)
         }
        
        status = ext_pyat.afegir_linia(st.session_state.token,
                                        st.session_state.id_base,
                                        st.session_state.id_t_Possessions,
                                        dades,
                                        columna_duplicats='Id_jugador')
        
    elif record == [] and st.session_state.estat_partida == 'En joc':
        st.error("De moment no es pot ingressar en una partida iniciada")
        time.sleep(2)
        
    else:
        st.session_state.id_jugador = record[0]['id']
    
    if 'id_jugador' in st.session_state:
        actualitzar_historic_jugador()
        st.session_state.ingres_partida = True
        actualitzar_possessions_restringides()

def creacio_callback():
    if st.session_state.nom_partida != "":
        #st.session_state.pantalla_inici = 'jugador'
        paquet_dades = pd.DataFrame([{
                        "Ronda": 0,
                        "Nombre de jugadors": 0,
                        "Economia": 0,
                        "Contaminació": 0,
                        "Salut": 0,
                        "Necessitats": 0,
                        "Recursos naturals": 100000,
                        "Recursos energètics": 100000,
                        "Nivell econòmic": 0,
                        "Nivell social": 0,
                        "Nivell mediambiental": -1}])
        
        dades_registre={
                        'Id': st.session_state.nom_partida+'_'+datetime.today().strftime('%Y-%m-%d'),
                        'Nom': st.session_state.nom_partida,
                        'Descripció': st.session_state.desc_partida,
                        'Estat': 'Per iniciar',
                        'dades':paquet_dades.to_json(orient='split',force_ascii=False)
                        }
        
        status1 = ext_pyat.afegir_linia(st.session_state.token,
                                        st.session_state.id_base,
                                        st.session_state.id_t_Registre_partides,
                                        dades_registre,
                                        columna_duplicats='Nom')
        if status1 == True:
            st.session_state.creacio = True
            st.session_state.estat_partida = 'Per iniciar'
            st.success('Partida creada')
        
        else:
            st.warning('Nom de partida ja existent')
        
        st.session_state.id_partida=ext_pyat.obtenir_id_record(st.session_state.token,
                                                               st.session_state.id_base,
                                                               st.session_state.id_t_Registre_partides,
                                                               columna = 'Nom',
                                                               coincidencia=st.session_state.nom_partida)
        st.button('Entrar com a administrador', on_click = acces_admin_callback)
            
    else:
        st.warning('Falta el nom de la partida empanat')


# %% Funcions de comprar

def guardar_t_possessions(input_df):
    #GUARDAR INFORMACIÓ A LA TAULA DE POSSESSIONS
    #Recollim el que hi havia prèviament
    record = ext_pyat.obtenir_record(st.session_state.token,st.session_state.id_base,st.session_state.id_t_Possessions,'Id_jugador',st.session_state.id_jugador)
    dades_previes = ext_pyat.obtenir_field_of_record(record[0],'dades',string_2_df=True)
    
    #Li afegim la marca de la ronda en la que es fa
    dades_noves = input_df
    dades_noves['Ronda'] = st.session_state.ronda_actual
    #Afegim les noves possessions a les que ja teniem
    df_total = pd.concat([dades_noves, dades_previes])
    #passem a dict
    paquet_dades = df_total
    #pugem a la taula de possessions
    dades = {'dades': paquet_dades.to_json(orient='split',force_ascii=False)}
    id_record = ext_pyat.obtenir_id_record(st.session_state.token,st.session_state.id_base,st.session_state.id_t_Possessions,'Id_jugador',st.session_state.id_jugador)
    ext_pyat.actualitzar_field_of_record(st.session_state.token,st.session_state.id_base,st.session_state.id_t_Possessions,id_record,dades)
    actualitzar_possessions_restringides()

def actualitzar_valors_jugador(input_df):
    #eliminem la columna de ronda perquè no sé perquè coi es sincronitza amb l'altra funció
    #que hi pugui haver per reduïr el nombre de caracter a guardar
    try:
        input_df = input_df.drop('Ronda', axis=1)
    except:
        pass
    
    print("l'input de la compra a dins la funció")
    print(input_df)
    
    #recollim lo nou i sumem els camps que es poden sumar
    qualitats_input_df = pd.DataFrame(input_df.sum(axis=0,numeric_only=True)).T
    print("qualitats_input_df")
    print(qualitats_input_df)
    #IMPORTANT!!! definim els signes de cada element ja que alguns es sumen i altres es resten
    #st.write(qualitats_input_df)
    qualitats_input_df = preparar_fusio(qualitats_input_df)
    print("qualitats despres de preparar fusió")
    print(qualitats_input_df)
    
    #sumem les columnes de la ronda en concret a lo que hem comprat
    dfsuma = pd.concat([qualitats_input_df, st.session_state.historic_jugador[st.session_state.historic_jugador["Ronda"] == st.session_state.ronda_actual]])
    dfsuma = dfsuma.sum(axis=0,numeric_only=True)
    print("el que s'ha de sumar")
    print(dfsuma)
    #substituim la fila
    st.session_state.historic_jugador.loc[st.session_state.historic_jugador[st.session_state.historic_jugador["Ronda"] == st.session_state.ronda_actual].index.tolist()[0]]=dfsuma
    print("el que pugem al servidor s'encalla?")
    print(st.session_state.historic_jugador)
    #passem a dict
    paquet_dades = st.session_state.historic_jugador
    #pugem a la taula de historic partides
    dades = {'dades': paquet_dades.to_json(orient='split',force_ascii=False)}
    ext_pyat.actualitzar_field_of_record(st.session_state.token,st.session_state.id_base,st.session_state.id_t_Historic_partides,st.session_state.id_jugador,dades)
    
    actualitzar_historic_jugador()

def guardar_accio_callback(inputdict):
    # S'utilitza quan l'usuari apreta el botó de guardar informació. És una funció previa al canvi de ronda
    #recollim lo nou i ho transformem en dataframe
    input_df = pd.DataFrame.from_dict(inputdict)
    print("l'input de la compra és:")
    print(input_df)
    #eliminem la columna de descripció que hi pugui haver per reduïr el nombre de caracter a guardar
    try:
        input_df = input_df.drop('Descripció', axis=1)
    except:
        pass
    #GUARDAR INFORMACIÓ A LA TAULA DE POSSESSIONS
    guardar_t_possessions(input_df)
    print("l'input de la compra després de guardar a possessions")
    print(input_df)
    #ACTUALITZAR VALORS DEL JUGADOR   
    actualitzar_valors_jugador(input_df)
 
# %% Funcions de passar ronda
    
def passar_ronda_jugador():
    
    #Agafem l'historic de dades del jugador que ja està al session state i dupliquem la ultima fila
    #Els canvis a fer són sumar 1 a la ronda, reestablir el temps de lleure i sumar el salari a l'economia
    ultima_fila=st.session_state.historic_jugador[st.session_state.historic_jugador['Ronda']==st.session_state.ronda_actual].reset_index(drop=True)
    #li fem els vancis oportuns a la fila
    ultima_fila.loc[0,('Ronda')]=ultima_fila.loc[0,('Ronda')]+1
    ultima_fila.loc[0,('Temps')] = min(ultima_fila.loc[0,('Temps')]+2,2)
    ultima_fila.loc[0,('Economia')] = ultima_fila.loc[0,('Economia')]+ultima_fila.loc[0,('Salari')]-(ultima_fila.loc[0,('Energia')] * st.session_state.f_energia_cost)
    ultima_fila.loc[0,('Recursos energètics')] = 0
    ultima_fila.loc[0,('Recursos naturals')] = 0
    ultima_fila.loc[0,('Aliments')] = ultima_fila.loc[0,('Aliments')] -1
    ultima_fila.loc[0,('Salut')] = ultima_fila.loc[0,('Salut')] -10
    ultima_fila.loc[0,('Contaminació')] = ultima_fila.loc[0,('Energia')] * st.session_state.f_energia_contaminacio
    
    #l'unim a la taula
    st.session_state.historic_jugador = pd.concat([st.session_state.historic_jugador,ultima_fila],ignore_index=True)
    
    #Transformem en json i pugem al servidor
    
    dades = {'dades': st.session_state.historic_jugador.to_json(orient='split',force_ascii=False)}
    ext_pyat.actualitzar_field_of_record(st.session_state.token,st.session_state.id_base,st.session_state.id_t_Historic_partides,st.session_state.id_jugador,dades)
    actualitzar_historic_jugador()
    st.session_state.ronda_actual = st.session_state.historic_jugador['Ronda'].max()

        
def funcio_espera_jugadors():
    #Esperem a que els altres jugadors finalitzin la ronda també

    actualitzar_historic_partida()

    while st.session_state.historic_partida.loc[:,'Ronda'].max() != st.session_state.ronda_actual:
        actualitzar_historic_partida()
        time.sleep(5)


def actualitzar_ronda_partida(ronda):
    df_partida_anterior = st.session_state.historic_partida[st.session_state.historic_partida['Ronda']==ronda -1].reset_index(drop=True)
    df_partida = st.session_state.historic_partida[st.session_state.historic_partida['Ronda']==ronda].reset_index(drop=True)
    df_jugador = st.session_state.df_jugadors[st.session_state.df_jugadors['Ronda']==ronda]
    #Preparem els valors de la fila actualitzada
    paquet_dades = pd.DataFrame([{
                                "Ronda": ronda,
                                "Nombre de jugadors": df_jugador.nunique()["id"],
                                "Economia": df_jugador["Economia"].sum(),
                                "Contaminació": df_partida_anterior["Contaminació"].sum() + df_jugador["Contaminació"].sum(),
                                "Salut": df_jugador["Salut"].mean(),
                                "Necessitats_transport": df_jugador["Necessitats_transport"].mean(),
                                "Necessitats_habitatge": df_jugador["Necessitats_habitatge"].mean(),
                                "Energia":df_jugador["Energia"].sum(),
                                "Temps":df_jugador["Temps"].sum(),
                                "Aliments":df_jugador["Aliments"].sum(),
                                "Salari":df_jugador["Salari"].mean(),
                                "PIB":df_partida_anterior["Economia"].sum()-(df_jugador["Economia"].sum()-df_jugador["Salari"].sum())+ df_jugador["Energia"].sum()* st.session_state.f_energia_cost,
                                "Nivell_individual":df_jugador["Nivell"].mean(),
                                "Recursos naturals": df_partida_anterior["Recursos naturals"].sum() + df_jugador["Recursos naturals"].sum(),
                                "Recursos energètics": df_partida_anterior["Recursos energètics"].sum() + df_jugador["Recursos energètics"].sum()- df_jugador["Energia"].sum(),
                                "Nivell econòmic": 0,
                                "Nivell social": 0,
                                "Nivell mediambiental": -1}])
    
    paquet_dades = paquet_dades.reindex(columns=st.session_state.historic_partida.columns)
    print('variable ronda')
    print(ronda)
    st.session_state.historic_partida.iloc[ronda] = paquet_dades.iloc[0].values
    print('imprimim el paquet de dades')
    print(st.session_state.historic_partida['Ronda']==ronda)
    print(paquet_dades)

def crear_ronda_partida():
    #Agafem l'historic de dades de la partida que ja està al session state i dupliquem la ultima fila
    #Els canvis a fer són sumar l'economia de les dades dels jugadors, el promig de la salut, afegir una ronda
    df_partida = st.session_state.historic_partida[st.session_state.historic_partida['Ronda']==st.session_state.ronda_actual].reset_index(drop=True)
    df_jugador = st.session_state.df_jugadors[st.session_state.df_jugadors['Ronda']==st.session_state.ronda_actual]
    #li fem els canvis oportuns a la fila
    df_partida.loc[0,('Economia')]= df_jugador["Economia"].sum()
    df_partida.loc[0,('Salut')] = df_jugador["Salut"].mean()
    df_partida.loc[0,('Ronda')] = st.session_state.ronda_actual +1

    
    #l'unim a la taula
    st.session_state.historic_partida = pd.concat([st.session_state.historic_partida,df_partida],ignore_index=True)
    


def passar_ronda_partida():
    #aquesta funció s'executarà constantment per tant cal posar un if que detecti
    # Recollim les rondes de tots els historics jugadors que tenim al df_jugadors
    rondes_actuals_jugadors = st.session_state.df_jugadors.groupby('nom jugador')['Ronda'].max()
    promig_rondes = rondes_actuals_jugadors.mean()
    st.session_state.ronda_actual = st.session_state.historic_partida['Ronda'].max()
    if promig_rondes == st.session_state.ronda_actual + 1:
        
        #actualitzem la fila de la partida amb els valors finals dels jugadors
        actualitzar_ronda_partida(int(st.session_state.ronda_actual))
        
        #creem una fila nova per la ronda entrant
        crear_ronda_partida()
        
        
        update_historic_partida()
        
        
        st.session_state.ronda_actual = st.session_state.ronda_actual +1
        
    else:
        pass

def update_historic_partida():
    # transformem en json i cap al servidor
    dades={"dades": st.session_state.historic_partida.to_json(orient='split',force_ascii=False)}
    print('dades de la partida')
    print(dades)
    ext_pyat.actualitzar_field_of_record(st.session_state.token,
                                         st.session_state.id_base,
                                         st.session_state.id_t_Registre_partides,
                                         st.session_state.id_partida,
                                         dades)

def restablir_taula_partida():
    rondes = st.session_state.ronda_actual
    print('La ronda actual és '+str(rondes))
    for ronda in range(int(rondes)-1):
        actualitzar_ronda_partida(ronda+1)
    update_historic_partida()
    
    

# %% Funcions càlculs

def carregar_factors_conversio():
    st.session_state.f_energia_cost = 1
    st.session_state.f_energia_contaminacio = 1

def inicialitzar_estatus_jugador():
    # Salari
    # Genera dos valors aleatoris de la distribució normal estàndard
    valor_aleatori_1 = np.random.rand()
    valor_aleatori_2 = np.random.rand()
    
    # Paràmetres per a la inversa de la distribució normal
    mitjana1, desviacio_estandard1 = 150, 30
    mitjana2, desviacio_estandard2 = 50, 1000
    
    # Calcula els valors inversos i aplica el valor absolut
    invers1 = abs(norm.ppf(valor_aleatori_1, loc=mitjana1, scale=desviacio_estandard1))
    invers2 = norm.ppf(valor_aleatori_2, loc=mitjana2, scale=desviacio_estandard2)
    
    # Calcula el màxim entre els dos valors
    Salari = max(invers1, invers2)+150
    # Economia
    # Genera un valor aleatori de la distribució normal estàndard
    valor_aleatori = np.random.rand()
    Economia = abs(norm.ppf(valor_aleatori, loc=100, scale=1000)) + Salari
    
    # Salut
    # Genera un nombre aleatori entre 0 i 1, i després escala i trasllada
    Salut = np.random.rand() * 50 + 50
    
    #Necessitats transport
    Necessitats_transport = calcul_necessitats_inicial(Salari)/100
    #Necessitats habitatge
    Necessitats_habitatge = calcul_necessitats_inicial(Salari)/100
    
    return Salari, Economia, Salut, Necessitats_transport, Necessitats_habitatge
    
def calcul_necessitats_inicial(Salari):
    # Genera un nombre aleatori entre 0 i 1
    valor_aleatori = np.random.rand()
    # Estructura condicional equivalent
    if valor_aleatori > 0.8:
        Necessitats = np.random.rand() * 30
    else:
        if Salari > 1000:
            Necessitats = 5
        else:
            Necessitats = 0
    return Necessitats
    
def preparar_fusio(df):
    print(df.columns.tolist())
    try:
        df = df.rename(columns={'Preu': 'Economia'})
    except:
        pass
    # Es prepararà el df canviant el signe dels camps d'acord a lo següent:
    signes = {"Contaminació": 1,
               "Aliments": 1,
               "Temps": -1,
               "Energia": 1,
               "Recursos energètics": -1,
               "Recursos naturals": -1,
               "Salut": 1,
               "Necessitats_habitatge": 1,
               "Necessitats_transport": 1,
               "Economia": -1}
    print(df.columns.tolist())
    for columna in df.columns.tolist():
        try:
            print(columna)
            df[columna] = df[columna].apply(lambda x: x*signes[columna])
        except:
            pass   
    return df
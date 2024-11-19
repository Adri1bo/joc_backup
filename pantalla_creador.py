# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 15:38:24 2024

@author: adria
"""
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import callbacks
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
    
def entra_crea():
    st.session_state.nom_partida = st.text_input('Introdueix el nom de la partida que vols crear')
    st.session_state.desc_partida = st.text_input('Descripció de la partida')
    st.button('Crea!', on_click=callbacks.creacio_callback)
    
def iniciar():
    st.write('Esperant als jugadors...')
    callbacks.df_jugadors_callback()
    #refresquem automaticament cada 5 segons
    st.write(st.session_state.df_jugadors)
    st.button('iniciar_partida',on_click = callbacks.iniciar_partida_callback)
    st.button('sortir partida', on_click = callbacks.sortir_partida_callback)
    count = st_autorefresh(interval=10 * 1000, limit=2000, key="fizzbuzzcounter")
    
def partida():
    callbacks.df_jugadors_callback()
    callbacks.actualitzar_historic_partida()
    st.header('Taula de jugadors')
    st.write(st.session_state.df_jugadors)
    st.header('Taula partida')
    st.write(st.session_state.historic_partida)
    st.button('sortir partida', on_click = callbacks.sortir_partida_callback)
    st.button('recalcular taula partida', on_click = callbacks.restablir_taula_partida)
    
    #Pantalla de dashboards
    df_jugadors_sorted = st.session_state.df_jugadors.sort_values(by='Salari',ascending = False)
    #dashboard de barres x = jugadors i y variable = contaminació, recursos materials, recursos energètics
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
    x=df_jugadors_sorted["nom jugador"],
    y=df_jugadors_sorted["Contaminació"],
    name='Contaminació',
    marker_color='grey'
    ))
    
    fig1.add_trace(go.Bar(
    x=df_jugadors_sorted["nom jugador"],
    y=df_jugadors_sorted["Recursos naturals"]*-1,
    name='Recursos naturals',
    marker_color='green'
    ))
    
    fig1.add_trace(go.Bar(
    x=df_jugadors_sorted["nom jugador"],
    y=df_jugadors_sorted["Recursos energètics"]*-1+df_jugadors_sorted["Energia"],
    name='Recursos energètics',
    marker_color='red'
    ))
    
    #fig1 = px.bar(st.session_state.df_jugadors, x="nom jugador", y="Contaminació")

    #gràfic de barres x = salari (ordenat) i y variable = contaminació, recursos materials, recursos energètics
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
    x=df_jugadors_sorted["Salari"],
    y=df_jugadors_sorted["Contaminació"],
    name='Contaminació',
    marker_color='grey'
    ))
    
    fig2.add_trace(go.Bar(
    x=df_jugadors_sorted["Salari"],
    y=df_jugadors_sorted["Recursos naturals"]*-1,
    name='Recursos naturals',
    marker_color='green'
    ))
    
    fig2.add_trace(go.Bar(
    x=df_jugadors_sorted["Salari"],
    y=df_jugadors_sorted["Recursos energètics"]*-1+df_jugadors_sorted["Energia"],
    name='Recursos energètics',
    marker_color='red'
    ))
    #gràfic lineal x = rondes yvariable = contaminació, recursos
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
    x=st.session_state.historic_partida["Ronda"],
    y=st.session_state.historic_partida["Contaminació"]/1000,
    name='Contaminació',
    marker_color='grey'
    ))
    
    
    #gràfic lineal x = rondes yvariable = recursos
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
    x=st.session_state.historic_partida["Ronda"],
    y=st.session_state.historic_partida["Recursos naturals"]/100000,
    name='Recursos naturals',
    marker_color='green'
    ))
    
    fig4.add_trace(go.Scatter(
    x=st.session_state.historic_partida["Ronda"],
    y=st.session_state.historic_partida["Recursos energètics"]/100000,
    name='Recursos energètics',
    marker_color='red'
    ))
    
    #gràfic lineal economia general
    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(
    x=st.session_state.historic_partida["Ronda"],
    y=st.session_state.historic_partida["Economia"],
    name='Economia',
    marker_color='grey'
    ))
    #gràfic linees economia per jugador
    fig6 = px.line(st.session_state.df_jugadors, x="Ronda", y="Economia", color = 'nom jugador')
    
    #grafic linees x= ronda y = PIB i contaminació
    
    fig7 = go.Figure()
    fig7.add_trace(go.Scatter(
    x=st.session_state.historic_partida["Ronda"],
    y=st.session_state.historic_partida["PIB"],
    name='PIB',
    marker_color='green'
    ))
    
    fig7.add_trace(go.Scatter(
    x=st.session_state.historic_partida["Ronda"],
    y=st.session_state.df_jugadors.groupby('Ronda')['Contaminació'].sum(),
    name='Contaminació emesa',
    marker_color='red'
    ))
    
    # grafic comparatiu necessitats dels jugadors
    
    

    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Impactes per jugador", "Impactes per salari","Evolució contaminació", "Evolució recursos", "Economia general","Economia jugadors","Economia i contaminació","Variables jugadors"])
    with tab1:
        # Use the Streamlit theme.
        # This is the default. So you can also omit the theme argument.
        st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
    with tab2:
        # Use the Streamlit theme.
        # This is the default. So you can also omit the theme argument.
        st.plotly_chart(fig2, theme="streamlit", use_container_width=True)
    with tab3:
        # Use the Streamlit theme.
        # This is the default. So you can also omit the theme argument.
        st.plotly_chart(fig3, theme="streamlit", use_container_width=True)
    with tab4:
        # Use the Streamlit theme.
        # This is the default. So you can also omit the theme argument.
        st.plotly_chart(fig4, theme="streamlit", use_container_width=True)
    with tab5:
        # Use the Streamlit theme.
        # This is the default. So you can also omit the theme argument.
        st.plotly_chart(fig5, theme="streamlit", use_container_width=True)
    with tab6:
        # Use the Streamlit theme.
        # This is the default. So you can also omit the theme argument.
        st.plotly_chart(fig6, theme="streamlit", use_container_width=True)
    with tab7:
        # Use the Streamlit theme.
        # This is the default. So you can also omit the theme argument.
        st.plotly_chart(fig7, theme="streamlit", use_container_width=True)
    with tab8:
        # Use the Streamlit theme.
        # This is the default. So you can also omit the theme argument.
        variable = st.selectbox('Escull variable',st.session_state.df_jugadors.columns.tolist())
        #variable2 = st.selectbox('Escull variable2',st.session_state.df_jugadors.columns.tolist())
        fig8 = px.line(st.session_state.df_jugadors, x='Ronda', y=variable, color='nom jugador')
        #fig8.add_trace(px.bar(st.session_state.df_jugadors, x='Ronda', y=variable2, color='nom jugador').update_traces(name='Line 2'))

        st.plotly_chart(fig8, theme="streamlit", use_container_width=True)
    
    callbacks.passar_ronda_partida()
    count = st_autorefresh(interval=20 * 1000, limit=2000, key="fizzbuzzcounter")
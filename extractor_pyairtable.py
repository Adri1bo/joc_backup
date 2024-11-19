# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 11:34:09 2023

@author: above
"""


from pyairtable import Api
import pandas as pd
import streamlit as st
from pyairtable.formulas import match
import json

def get_taula(token,id_base,id_taula):
    api = Api(token)
    table = api.table(id_base, id_taula)
    taula = table.all()
    return table, taula
    
def obtenir_credencials(token,id_base,id_taula):
    table, taula = get_taula(token,id_base,id_taula)
    credencials=''
    #Unim tots els camps de credencials que hi ha
    for i in range(len(taula)):
        credencials = taula[i]['fields']['Notes'] + credencials
    

    contingut = eval(credencials)
    
    dict_contenidor={'cookie': {'expiry_days': 30,'key':'random_signature_key','name': 'random_cookie_name'},'credentials': {''},'preauthorized': {'emails': ['melsby@gmail.com']}}
    
    dict_contenidor['credentials']=contingut
    content=dict_contenidor
    
    return content

def actualitzar_credencials(token,id_base,id_taula,noves_credencials):
    table, taula = get_taula(token,id_base,id_taula)
    
    #Dividim les noves credencials en trossots de 50000
    step=50000
    divisor=len(noves_credencials)//step + 1
    for i in range(divisor):
        noves_credencials[step*i:step*(i+1)]
        id_record = taula[i]['id']
        table.update(id_record, {"Notes": noves_credencials})
    
def validar_mail_registre(token,id_base,id_taula,noves_credencials):
    #primer obtenim totes les credencials de la base de dades del servidor
    credencials = obtenir_credencials(token,id_base,id_taula)['credentials']
    
    
    #comparem el string amb les noves credencials

    diferencia=str(noves_credencials)[len(str(credencials)):-2]
    diferencia_dict = eval('{'+diferencia+'}')

    #obtenim el mail que es vol registrar
    key = list(diferencia_dict.keys())[0]
    nou_mail = diferencia_dict[key]['email']
    
    #revisem que no existixi ja
    usuaris = list(credencials['usernames'].keys())
    emails=[credencials['usernames'][i]['email'] for i in usuaris]
    
    if nou_mail in emails:
        #no es pot fer servir aquest correu
        validacio=0
    else:
        #cap problema seguim amb el registre
        validacio=1
    
    return validacio  
    
    
def obtenir_taula(token,id_base,id_taula,columna_filtre=None,v_columna_filtre=None):
    table, taula = get_taula(token,id_base,id_taula)
    
    #transformem el dict en una taula de pandas
    taula_dades=[taula[i]['fields'] for i in range(len(taula))]
    taula_id=[ taula[i]['id'] for i in range(len(taula))]

    for i in range(len(taula)):
        taula_dades[i]['id'] = taula_id[i]
        taula_dades[i]=dict(sorted(taula_dades[i].items()))
        
    df = pd.DataFrame(taula_dades)
    try:
        df = df[df[columna_filtre] == v_columna_filtre]
    except:
        pass
    
    return df, table

def afegir_linia(token,id_base,id_taula,dades,columna_duplicats=None,columna_filtre=None,v_columna_filtre=None):
    df, table = obtenir_taula(token,id_base,id_taula)
    

    #revisem si el nou nom està a dins de la df a la columna indicada a duplicats
    #apliquem el filtre primer
    try:
        df = df[df[columna_filtre] == v_columna_filtre]
    except:
        pass
    duplicat=dades[columna_duplicats] in df[columna_duplicats].unique()

   
    if duplicat==True:
        status = False
    else:
        #Creem la nova línia
        table.create(dades)
        status=True
    return status
 
def obtenir_record(token,id_base,id_taula,columna,coincidencia):
    """
    Aquesta funció filtra una taula per un o varis arguments i retorna el record o records resultants

    Parameters
    ----------
    token : str
        token per accedir a la base.
    id_base : str
        ide de la base del pyairtable.
    id_taula : str
        ide de la taula que vols filtrar.
    columna : list of str
        noms de les columnes a filtrar.
    coincidencia : list of values or strings
        valors a filtrar per la columna indicada.

    Returns
    -------
    record : és un dict
        retorna una línia o varies de la taula en forma de dict.

    """
    table, taula = get_taula(token,id_base,id_taula)
    
    #transformem en llistes els inputs de columna i coincidencia si no ho son
    if type(columna) is not list:
        columna = [columna]
        
    if type(coincidencia) is not list:
        coincidencia = [coincidencia]
          
    #convertim les llistes en unn dict perpoder fer un filtratge multiple
    res = dict(zip(columna, coincidencia))
    formula = match(res)
    record=table.all(formula=formula)
    return record
   
def obtenir_id_record(token,id_base,id_taula,columna,coincidencia):
    record=obtenir_record(token,id_base,id_taula,columna,coincidencia)
    Id = record[0]['id']
    return Id
    
def obtenir_field_of_record(record,camp,string_2_df=False):
    fields = record['fields']
    field = fields[camp]
    if string_2_df == True:
        field = split_json_to_df(field)
    return field

def obtenir_record_per_id(token,id_base,id_taula,id_record):
    df, table = obtenir_taula(token,id_base,id_taula)
    record = table.get(id_record)
    return record

def actualitzar_field_of_record(token,id_base,id_taula,id_record,dades):
    table, taula = get_taula(token,id_base,id_taula)
    table.update(id_record, dades)
    
def split_json_to_df(split_json):
    split_json = json.loads(split_json)
    df = pd.json_normalize(split_json, 'data')

    # Assigna manualment les columnes i l'índex
    df.columns = split_json['columns']
    df['index'] = split_json['index']
    df.set_index('index', inplace=True)
    return df